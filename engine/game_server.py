import itertools
import math
import random

from engine.schema import defenses_dict, attacks_dict, VISIBLE_DEFENSES, VISIBLE_ATTACKS
from engine.logic import Logic 

# Random values for now
GAME_MODE_SETTINGS = {
    "BEGINNER": {"starting_health": 100, "starting_budget": 700},
    "CUSTOM": {"starting_health": 125, "starting_budget": 1000},
    "RANDOM": {"starting_health": 100, "starting_budget": 700},
}

RANDOM_STARTING_DEFENSES = 10
RANDOM_DEFENSES_UNLOCKED_PER_LEVEL = 5
RANDOM_MIN_ATTACKS = 1
RANDOM_MAX_ATTACKS = 3

class GameServer:
    """
    Core functionality about game stats, player moves, attack moves, and level status.
    """

    def __init__(self):
        """
        Sets up the basic server instance and waits for connections/commands.
        """
        print("[SERVER] Initializing MITRE ATT&CK Game Server...")

        # initialize logic  
        self.logic = Logic()
        self.available_defenses = filtered_defenses = {
            key: defenses_dict[key] 
            for key in VISIBLE_DEFENSES 
            if key in defenses_dict
        }
        self.available_attacks = filtered_defenses = {
            key: attacks_dict[key] 
            for key in VISIBLE_ATTACKS 
            if key in attacks_dict
        }
        
        # --- Feature 3.b: Game environment variables ---
        self.state = "AWAITING_START"
        self.level = 1
        self.game_mode = "BEGINNER"
        self.random_defense_order = []
        self.random_required_defenses = set()
        # Random attacks are dealt from this pool without repetition.
        # A new shuffled cycle begins only after every attack in the current
        # eligible pool has been used.
        self.random_attack_remaining = []
        
        # Player Status 
        self.player_health = 100 # health is a tuple where (health, shield) - the shield is bonus health
        self.player_shield = 0
        self.player_budget = 700
        self.active_defenses = {}
        self.number_failures = 0

        # Attack Status
        self.current_level_attacks = []
        self.is_running = True

        # Feedback Status
        self.feedback_title = ""
        self.feedback_body = ""

    def is_final_level(self):
        """Return True when the current mode has reached its last level.

        Random mode is endless: once every defense has been unlocked, later
        levels continue with new randomized attacks and a freshly reset board.
        """
        if self.game_mode == "RANDOM":
            return False
        return self.level >= 3

    def _reset_level_resources(self):
        """Reset resources that should not carry between Random mode levels."""
        settings = GAME_MODE_SETTINGS[self.game_mode]
        self.active_defenses = {}
        self.number_failures = 0

    def _minimum_required_defenses_for_attacks(self, attack_ids):
        """Return the cheapest cabinet-available defense set for Random attacks.

        Random mode scores an attack against only the matching defenses that are
        currently available in the cabinet. The player must place at least 70%
        of those available matching defenses.

        To keep attacks with very large mitigation lists from appearing with only
        one useful option, any attack that has 3 or more total mapped defenses
        must have at least 3 corresponding defenses available in the cabinet.
        Attacks with only 1-2 total mapped defenses may appear when at least one
        matching defense is available.
        """
        required_union = set()

        for attack_id in attack_ids:
            attack = attacks_dict[attack_id]
            all_mitigations = list(dict.fromkeys(getattr(attack, "defenses", []) or []))

            # Preserve the existing behavior for attacks with no listed mitigations.
            if not all_mitigations:
                continue

            available_matching = [
                key for key in all_mitigations if key in self.available_defenses
            ]

            # Large mitigation lists need at least three usable cabinet options.
            if len(all_mitigations) >= 3:
                if len(available_matching) < 3:
                    return None
            elif not available_matching:
                return None

            defenses_needed = math.ceil(0.70 * len(available_matching))

            cheapest = sorted(
                available_matching,
                key=lambda key: self.available_defenses[key].cost,
            )[:defenses_needed]
            required_union.update(cheapest)

        total_cost = sum(
            self.available_defenses[key].cost for key in required_union
        )
        return required_union, total_cost

    def _globally_defendable_random_attacks(self):
        """Return attacks that can be mitigated once the full defense catalog is unlocked."""
        original_available = self.available_defenses
        self.available_defenses = dict(defenses_dict)
        try:
            return [
                attack_id
                for attack_id in attacks_dict
                if self._minimum_required_defenses_for_attacks([attack_id]) is not None
            ]
        finally:
            self.available_defenses = original_available

    def _start_random_attack_cycle(self):
        """Shuffle the full valid attack catalog for a new no-repeat cycle."""
        eligible = self._globally_defendable_random_attacks()
        if not eligible:
            raise RuntimeError(
                "Random mode has no attacks with valid defendable mitigation mappings."
            )
        random.shuffle(eligible)
        self.random_attack_remaining = eligible

    def _choose_defendable_random_attacks(self):
        """Choose a fully defendable 1-3 attack set without repeats.

        The attack count is random among the counts that are actually possible
        with the currently unlocked defenses. Every candidate combination is
        validated as a whole before it can be selected. Used attacks are removed
        from the current cycle and cannot return until the cycle is exhausted.
        """
        if not self.random_attack_remaining:
            self._start_random_attack_cycle()

        # First keep only unused attacks that can be defended on their own.
        defendable_unused = [
            attack_id
            for attack_id in self.random_attack_remaining
            if self._minimum_required_defenses_for_attacks([attack_id]) is not None
        ]

        if not defendable_unused:
            return None, None, None

        # Build valid combinations for each possible attack count.
        # This prevents a level from receiving attacks that are individually
        # defendable but impossible to defend together.
        valid_by_count = {}
        max_count = min(RANDOM_MAX_ATTACKS, len(defendable_unused))

        for count in range(RANDOM_MIN_ATTACKS, max_count + 1):
            valid_combinations = []
            for combo in itertools.combinations(defendable_unused, count):
                required_info = self._minimum_required_defenses_for_attacks(combo)
                if required_info is not None:
                    valid_combinations.append((list(combo), required_info))

            if valid_combinations:
                valid_by_count[count] = valid_combinations

        if not valid_by_count:
            return None, None, None

        # Randomly choose 1, 2, or 3 attacks from the counts that are currently
        # feasible, rather than defaulting to one attack when multiple are possible.
        chosen_count = random.choice(list(valid_by_count.keys()))
        chosen, required_info = random.choice(valid_by_count[chosen_count])

        chosen_set = set(chosen)
        self.random_attack_remaining = [
            attack_id
            for attack_id in self.random_attack_remaining
            if attack_id not in chosen_set
        ]

        required_set, minimum_cost = required_info
        return chosen, required_set, minimum_cost

    def _ensure_random_budget(self, minimum_cost):
        """Carry budget forward, topping it up only when the next level needs more."""
        if self.player_budget < minimum_cost:
            self.player_budget += minimum_cost - self.player_budget

    def _set_random_available_defenses(self, unlocked_count):
        """Build the cumulative cabinet for this level.

        Previously unlocked defenses stay fixed. Newly unlocked slots remain random,
        but their order may be rerolled when needed to make at least one still-unused
        attack from the current no-repeat cycle defendable.
        """
        total_defenses = len(defenses_dict)
        unlocked_count = min(unlocked_count, total_defenses)

        if not self.random_defense_order:
            self.random_defense_order = list(defenses_dict.keys())
            random.shuffle(self.random_defense_order)

        unlocked_keys = self.random_defense_order[:unlocked_count]
        self.available_defenses = {
            key: defenses_dict[key] for key in unlocked_keys
        }
        self.available_attacks = attacks_dict

    def _setup_random_level(self):
        """Unlock defenses and create a defendable, no-repeat Random level."""
        total_defenses = len(defenses_dict)
        unlocked_count = min(
            total_defenses,
            RANDOM_STARTING_DEFENSES
            + (self.level - 1) * RANDOM_DEFENSES_UNLOCKED_PER_LEVEL,
        )

        if not self.random_attack_remaining:
            self._start_random_attack_cycle()

        # Keep all defenses that were already unlocked on the previous level. Only
        # the still-locked tail is rerolled, preserving cumulative progression.
        previous_unlocked_count = min(
            total_defenses,
            RANDOM_STARTING_DEFENSES
            + max(0, self.level - 2) * RANDOM_DEFENSES_UNLOCKED_PER_LEVEL,
        ) if self.level > 1 else 0

        fixed_prefix = self.random_defense_order[:previous_unlocked_count]
        if not self.random_defense_order:
            fixed_prefix = []

        all_keys = list(defenses_dict.keys())
        locked_keys = [key for key in all_keys if key not in fixed_prefix]

        # Try random arrangements of the newly unlocked defenses until at least one
        # unused attack from the current cycle can be defended.
        for _ in range(1000):
            random.shuffle(locked_keys)
            candidate_order = fixed_prefix + locked_keys
            self.random_defense_order = candidate_order
            self._set_random_available_defenses(unlocked_count)

            chosen_attacks, required_set, minimum_cost = self._choose_defendable_random_attacks()
            if chosen_attacks is not None:
                self.current_level_attacks = chosen_attacks
                self.random_required_defenses = set(required_set)
                self._ensure_random_budget(minimum_cost)
                return

        # If all defenses are unlocked and we still cannot deal a card, the schema
        # has an attack whose mitigation mapping cannot satisfy the 70% rule.
        raise RuntimeError(
            "Random mode could not make an unused attack defendable with this "
            "level's unlocked defenses. Check attack mitigation mappings."
        )

    def setup_current_level(self):
        """Prepare attacks and defenses according to the selected game mode."""
        if self.game_mode == "RANDOM":
            self._setup_random_level()
        else:
            self.current_level_attacks = self.logic.get_level_attacks(
                self.level, self.available_attacks
            )

    # --- Feature 3.d: Game play handler functions ---
    
    def handle_build_defense(self, defense_key):
        """Handles the logic of a player buying/placing a defense."""
        try: 
            # Pass dict keys as a list
            new_budget = self.logic.process_purchase(
                defense_key, 
                self.player_budget, 
                list(self.active_defenses.keys()) 
            )
            self.player_budget = new_budget
            defense = self.available_defenses[defense_key]
            
            # Track which level the defense was placed on
            self.active_defenses[defense_key] = self.level 
            
            return f"[SERVER] Defense '{defense.name}' built successfully."
        except ValueError as e:
            return f"[SERVER] ERROR: {str(e)}"
        
    def handle_remove_defense(self, defense_key):
        """Handles the logic of a player removing a defense and refunding their budget."""
        if defense_key in self.active_defenses:
            defense = self.available_defenses[defense_key]
            self.player_budget += defense.cost
            del self.active_defenses[defense_key]
            return f"[SERVER] Defense '{defense.name}' removed. ${defense.cost} refunded."
        return f"[SERVER] ERROR: Defense '{defense_key}' is not active."

    def handle_launch_attack(self):
        """Handles the logic of the attacker launching a specific APT vector."""
        attacks = self.current_level_attacks
        if not self.current_level_attacks:
            f"[SERVER] ERROR: No attacks'."
        # launch every attack for this level 
        for attack in self.current_level_attacks:
            if attack in self.available_attacks:
                return f"[SERVER] Attack '{self.available_attacks[attack].name}' launched."
            return f"[SERVER] ERROR: Invalid attack '{attack}'."
        
    def handle_generate_failure_hint(self):
        return self.logic.generate_failure_hint(
            self.current_level_attacks,
            list(self.active_defenses.keys()),
            self.player_budget,
            available_defenses=self.available_defenses,
        )
    
    def handle_get_victory_message(self):
        return self.logic.generate_victory_message(self.current_level_attacks, list(self.active_defenses.keys()))
    
    def handle_game_over_message(self): 
        return self.logic.generate_game_over_message(self.current_level_attacks, self.active_defenses, self.available_defenses)

    def resolve_round(self):
        """Calculates score, rewards, and penalties based on active defenses."""
        if not self.current_level_attacks:
            return "[SERVER] ERROR: No attack was launched."

        # 1. Get score from logic 
        if self.game_mode == "RANDOM":
            score = self.logic.calculate_round_results(
                self.current_level_attacks,
                list(self.active_defenses.keys()),
                available_defenses=self.available_defenses,
            )
        else:
            score = self.logic.calculate_round_results(
                self.current_level_attacks,
                list(self.active_defenses.keys()),
                available_defenses=self.available_defenses,
            )
        
        success = self.logic.determine_success(score)
        
        if success:
            attacks_str = ", ".join(self.current_level_attacks)
            result_msg = f"[SERVER] SUCCESS: Attacks '{attacks_str}' were BLOCKED. (+250 Budget, +25 Health)"
            self.number_failures = 0
        else:
            attacks_str = ", ".join(self.current_level_attacks)
            result_msg = f"[SERVER] FAILURE: Attacks '{attacks_str}' SUCCEEDED."
            self.state = "LEVEL_FAILED"
            self.number_failures = self.number_failures + 1
        
        # update budget and health according to the logic
        self.player_health = self.logic.calculate_new_health(self.player_health, self.number_failures, success)
        self.player_budget = self.logic.calculate_new_budget(self.player_budget, self.number_failures, success)
        
        # Check for Game Over, else move to transition states (level failed or next level)
        if self.player_health <= 0:
            self.state = "GAME_OVER"
            return result_msg + "\n[SERVER] SYSTEM COMPROMISED. Health reached 0. GAME OVER."
        elif self.state == "LEVEL_FAILED":
            return result_msg + f"\n[SERVER] Level Failed. You must pass the level to move on. State: BUILD_PHASE. Level: {self.level}"
        else:
            self.state = "NEXT_LEVEL"
            return result_msg + "\n[SERVER] Transitioning to State: NEXT_LEVEL."
    
    def reset_server(self):
        """Restores the server to the title screen using the selected mode's defaults."""
        settings = GAME_MODE_SETTINGS[self.game_mode]
        self.player_health = settings["starting_health"]
        self.player_shield = 0
        self.player_budget = settings["starting_budget"]
        self.level = 1
        self.state = "AWAITING_START"
        self.active_defenses = {}
        self.current_level_attacks = []
        self.number_failures = 0
        self.random_defense_order = []
        self.random_required_defenses = set()
        self.available_defenses = {
            key: defenses_dict[key]
            for key in VISIBLE_DEFENSES
            if key in defenses_dict
        }
        self.available_attacks = {
            key: attacks_dict[key]
            for key in VISIBLE_ATTACKS
            if key in attacks_dict
        }
        return "[SERVER] System Rebooted. All parameters initialized to Level 1."

    def handle_custom_game_start(self, selected_attacks, selected_defenses):
        self.available_defenses = {
            tag: defenses_dict[tag]
            for tag in selected_defenses
            if tag in defenses_dict
        }

        # Build available_attacks as a dictionary { "ID": Attack(...) }
        self.available_attacks = {
            tag: attacks_dict[tag]
            for tag in selected_attacks
            if tag in attacks_dict
        }

        unmitigated_attacks = self.logic.validate_custom_attacks_and_defenses(self.available_attacks, self.available_defenses)  

        return unmitigated_attacks      
        #self.player_budget = self.logic.calculate_necessary_custom_budget(selected_attacks, selected_defenses)

    def parse_command(self, command):
        """
        Parses raw string inputs simulating network packets from Attack/Defense scripts.
        """
        cmd_parts = command.strip().split(" ", 1)
        action = cmd_parts[0].upper()
        payload = cmd_parts[1] if len(cmd_parts) > 1 else ""

        #Added Game mode stuff
        if action == "START_GAME":
            requested_mode = payload.strip().upper() or "BEGINNER"
            if requested_mode not in GAME_MODE_SETTINGS:
                return f"[SERVER] ERROR: Unknown game mode '{requested_mode}'."

            self.game_mode = requested_mode
            settings = GAME_MODE_SETTINGS[self.game_mode]

            #Start all new games with level 1 settings
            self.level = 1
            self.player_health = settings["starting_health"]
            self.player_shield = 0
            self.player_budget = settings["starting_budget"]
            self.active_defenses = {}
            self.number_failures = 0
            self.feedback_title = ""
            self.feedback_body = ""
            self.random_defense_order = []
            self.random_required_defenses = set()

            # Restore the standard pools before applying a mode-specific setup.
            self.available_defenses = {
                key: defenses_dict[key]
                for key in VISIBLE_DEFENSES
                if key in defenses_dict
            }
            self.available_attacks = {
                key: attacks_dict[key]
                for key in VISIBLE_ATTACKS
                if key in attacks_dict
            }

            if self.game_mode == "CUSTOM":
                self.state = "CUSTOM_DESIGN_PHASE"
            else:
                self.state = "BUILD_PHASE"
                self.setup_current_level()
                return (
                    f"[SERVER] The game has been started in {self.game_mode} mode. "
                    f"Starting Level {self.level}. Health: {self.player_health}. "
                    f"Budget: {self.player_budget}. Target Attack(s): "
                    f"{self.current_level_attacks}. State: BUILD_PHASE "
                )
            return(
                f"[SERVER] The game has been started in {self.game_mode} mode. "
                f"Awaiting custom defenses and attacks."
            )

        elif action == "START_CUSTOM":
            if self.state == "CUSTOM_DESIGN_PHASE":
                # Extract comma-separated lists from payload: "ATTACKS:a1,a2 DEFENSES:d1,d2"
                chosen_attacks = []
                chosen_defenses = []

                if "ATTACKS:" in payload:
                    atk_part = payload.split("ATTACKS:")[1].split(" ")[0]
                    if atk_part.strip():
                        chosen_attacks = [a.strip() for a in atk_part.split(",") if a.strip()]
                if not chosen_attacks:
                    return (
                        f"ERROR: Game not started. No attacks chosen."
                    ) 

                if "DEFENSES:" in payload:
                    def_part = payload.split("DEFENSES:")[1].split(" ")[0]
                    if def_part.strip():
                        chosen_defenses = [d.strip() for d in def_part.split(",") if d.strip()]

                # Execute logic and update server state
                unmitigated_attacks = self.handle_custom_game_start(chosen_attacks, chosen_defenses)
                if not unmitigated_attacks: 
                    self.state = "BUILD_PHASE"
                    self.current_level_attacks = self.logic.get_level_attacks(self.level, self.available_attacks)
                    self.player_budget = self.logic.calculate_budget_for_attack(self.current_level_attacks[0], self.available_defenses, defenses_dict, attacks_dict)
                    return (
                        f"Starting Level {self.level}. Health: {self.player_health}. "
                        f"Budget: {self.player_budget}. Target Attack(s): "
                        f"{self.current_level_attacks}. State: BUILD_PHASE\n"
                        f"Attacks: {list(self.available_attacks.keys())} | Defenses: {list(self.available_defenses.keys())} | Unmitigated: {list(unmitigated_attacks)}" 
                    )
                else:
                   # Helper to format dict/keys into readable "Key (Name)" strings
                    unmitigated_str = "\n".join(
                        f"• {k}: {attacks_dict[k].name}" if k in attacks_dict and hasattr(attacks_dict[k], 'name') else f"• {k}"
                        for k in unmitigated_attacks
                    ) or "• None"

                    return (
                        f"ERROR: Cannot start game. The selected defenses cannot mitigate the following attack(s):\n"
                        f"{unmitigated_str}"
                    )
            else:
                return "[SERVER] Action Denied. Not in Custom Design Phase."
        elif action == "BUILD_DEFENSE":
            if self.state == "BUILD_PHASE":
                return self.handle_build_defense(payload)
            else:
                return "[SERVER] Action Denied. Not in Build Phase."

        elif action == "LOCK_DEFENSES":
            if self.state == "BUILD_PHASE":
                self.state = "ATTACK_PHASE"
                return "[SERVER] Defenses Locked. Transitioning to State: ATTACK_PHASE"
            else:
                return f"[SERVER] Invalid Command for state: {self.state}."

        elif action == "LAUNCH_ATTACK":
            if self.state == "ATTACK_PHASE":
                return self.handle_launch_attack()
            else:
                return "[SERVER] Action Denied. Not in Attack Phase."

        elif action == "RESOLVE_ROUND":
            if self.state == "ATTACK_PHASE":
                return self.resolve_round()
            else:
                return f"[SERVER] Invalid Command for state: {self.state}."
        elif action == "RETRY_LEVEL":
            if self.state == "LEVEL_FAILED":
                # A retry stays on the same Random level and preserves damage.
                # Full resource/board resets happen only after a successful level,
                # allowing repeated failures to eventually reach GAME_OVER.
                self.state = "BUILD_PHASE"
                return f"[SERVER] Level restarted: {self.level}. State: {self.state}"
            else:
                return f"[SERVER] Invalid Command for state: {self.state}."
        elif action == "NEXT_LEVEL":
            if self.state == "NEXT_LEVEL":
                previous_level = self.level
                self.level += 1
                self.state = "BUILD_PHASE"
                if self.game_mode == "RANDOM":
                    self._reset_level_resources()
                self.setup_current_level()
                return (
                    f"[SERVER] Level {previous_level} Complete. Initializing Level {self.level}. "
                    f"Available Defenses: {len(self.available_defenses)}. "
                    f"Target Attacks: {self.current_level_attacks}, State: BUILD_PHASE"
                )
            else:
                return f"[SERVER] Cannot advance level from state: {self.state}."
        elif action == "REMOVE_DEFENSE":
            if self.state == "BUILD_PHASE":
                return self.handle_remove_defense(payload)
            else:
                return "[SERVER] Action Denied. Can only remove defenses during Build Phase."
        elif action == "STATUS":
            return f"[SERVER STATUS] Mode: {self.game_mode} | Level: {self.level} | Health: {self.player_health} | Shield: {self.player_shield} | Budget: {self.player_budget} | State: {self.state}"
        elif action == "EXIT":
            self.is_running = False
            return "[SERVER] Shutting down."
        elif action == "GET_FEEDBACK":
            if self.state == "GAME_OVER":
                self.feedback_title, self.feedback_body = self.handle_game_over_message()
                return f"{self.feedback_title}: {self.feedback_body}"
            elif self.state == "LEVEL_FAILED":
                self.feedback_title, self.feedback_body = self.handle_generate_failure_hint()
                return f"{self.feedback_title}: {self.feedback_body}"    
            elif self.state == "NEXT_LEVEL":
                self.feedback_title, self.feedback_body = self.handle_get_victory_message()
                return f"Level Passed: {self.feedback_body}"
            else:
                return f"Cannot give hint from state: {self.state}."
        else:
            return f"[SERVER] Unknown command: {command}"

    def run(self):
        """
        Main server loop waiting for input.
        """
        print(f"[SERVER] Server online. State: {self.state}")
        print("[INFO] Waiting for 'START_GAME' command ...")
        
        while self.is_running:
            try:
                incoming_command = input(">> ")
                response = self.parse_command(incoming_command)
                print(response)
            except KeyboardInterrupt:
                print("\n[SERVER] Force shutdown.")
                break

if __name__ == "__main__":
    server = GameServer()
    server.run()
