import sys
from engine.schema import defenses_dict, attacks_dict
from engine.logic import Logic 

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
        
        # --- Feature 3.b: Game environment variables ---
        self.state = "AWAITING_START"
        self.level = 1
        
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
            defense = defenses_dict[defense_key]
            
            # Track which level the defense was placed on
            self.active_defenses[defense_key] = self.level 
            
            return f"[SERVER] Defense '{defense.name}' built successfully."
        except ValueError as e:
            return f"[SERVER] ERROR: {str(e)}"
        
    def handle_remove_defense(self, defense_key):
        """Handles the logic of a player removing a defense and refunding their budget."""
        if defense_key in self.active_defenses:
            defense = defenses_dict[defense_key]
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
            if attack in attacks_dict:
                return f"[SERVER] Attack '{attacks_dict[attack].name}' launched."
            return f"[SERVER] ERROR: Invalid attack '{attack}'."
        
    def handle_generate_failure_hint(self):
        return self.logic.generate_failure_hint(self.current_level_attacks, list(self.active_defenses.keys()), self.player_budget)
    
    def handle_get_victory_message(self):
        return self.logic.generate_victory_message(self.current_level_attacks, list(self.active_defenses.keys()))
    
    def handle_game_over_message(self): 
        return self.logic.generate_game_over_message(self.current_level_attacks, self.active_defenses)

    def resolve_round(self):
        """Calculates score, rewards, and penalties based on active defenses."""
        if not self.current_level_attacks:
            return "[SERVER] ERROR: No attack was launched."

        # 1. Get score from logic 
        score = self.logic.calculate_round_results(self.current_level_attacks, list(self.active_defenses.keys()))
        
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
        """Restores the server to initial Level 1 state."""
        self.player_health = 100
        self.player_shield = 0
        self.player_budget = 1000
        self.level = 1
        self.state = "AWAITING_START"
        self.active_defenses = {}
        self.current_level_attacks = []
        self.number_failures = 0
        return "[SERVER] System Rebooted. All parameters initialized to Level 1."

    def parse_command(self, command):
        """
        Parses raw string inputs simulating network packets from Attack/Defense scripts.
        """
        cmd_parts = command.strip().split(" ", 1)
        action = cmd_parts[0].upper()
        payload = cmd_parts[1] if len(cmd_parts) > 1 else ""

        # --- Feature 3.c: Game Flow Control ---
        if action == "START_GAME":
            self.state = "BUILD_PHASE"
            self.current_level_attacks = self.logic.get_level_attacks(self.level)
            return f"[SERVER] The game has been started. Starting Level {self.level}. Target Attack(s): {self.current_level_attacks}. State: BUILD_PHASE"

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
                self.state = "BUILD_PHASE"
                return f"[SERVER] Level restarted: {self.level}. State: {self.state}"
            else:
                return f"[SERVER] Invalid Command for state: {self.state}."
        elif action == "NEXT_LEVEL":
            if self.state == "NEXT_LEVEL":
                self.level += 1
                self.state = "BUILD_PHASE"
                self.current_level_attacks = self.logic.get_level_attacks(self.level)  
                return f"[SERVER] Level {self.level-1} Complete. Initializing Level {self.level}. Target Attacks: {self.current_level_attacks}, State: BUILD_PHASE"
            else:
                return f"[SERVER] Cannot advance level from state: {self.state}."
        elif action == "REMOVE_DEFENSE":
            if self.state == "BUILD_PHASE":
                return self.handle_remove_defense(payload)
            else:
                return "[SERVER] Action Denied. Can only remove defenses during Build Phase."
        elif action == "STATUS":
            return f"[SERVER STATUS] Level: {self.level} | Health: {self.player_health} | Shield: {self.player_shield} | Budget: {self.player_budget} | State: {self.state}"
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
