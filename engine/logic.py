import random 
from engine.schema import defenses_dict, attacks_dict



class Logic:

    # function that chooses a random attack to be used in a phase and return the attack's id 
    @staticmethod
    def get_random_attack():
        return random.choice(list(attacks_dict.keys()))
    
    # function to return list of unique attack ids for that level 
    # Level 1 = 1 attack, Level 2 = 2 attacks, Level 3 = 3 attacks 
    def get_level_attacks(self, level_number):
        attack_ids = list(attacks_dict.keys())
        count = min(level_number, len(attack_ids))
        return random.sample(attack_ids, count)
    
    # Check if a defense can be purchased (return updated budget after defence is purchased)
    def process_purchase (self, defense_key, current_budget, active_defenses):

        # check if defense exists in list of possible defenses
        if defense_key not in defenses_dict:
            raise ValueError(f"Defense '{defense_key}' is not a valid MITRE defense.")
        defense = defenses_dict[defense_key]

        # check if the defense already exists 
        if defense_key in active_defenses:
            raise ValueError(f"Defense '{defense.name}' is already deployed.") 
               
        # check if there is enough money to purchase the defense 
        if current_budget < defense.cost:
            raise ValueError(f"Insufficient funds: Need {defense.cost}, have {current_budget}")
        
        # return updated budget if passes all checks 
        return current_budget - defense.cost
    
    # function to check if the defenses defend the attack accurately 

    def calculate_round_results(self, attack_ids, player_defenses):
        score = 0
        for attack_id in attack_ids: 
            attack = attacks_dict.get(attack_id)

            # check if attack exists
            if not attack:
                return 0
            
            required_defenses = attack.defenses 
            # check if defenses are needed, if not 100% success 
            if not required_defenses:
                return 100
            
            # score is calculated by the (# required defenses implemented / # required defenses) * 100
            matches = [d for d in player_defenses if d in required_defenses]
            score = (len(matches)/len(required_defenses)) * 100 

        return score 
    
    # Success (pass round) if score >= 70

    def determine_success(self, score):
        return score >= 70
    
    """
    Health Logic (logic resets everyround, health carries over):
    ### note the number of failures inclues the current failure 
    +25 if success 
    -25 if failure 1
    -50 if failure 2
    -75 if failure 3
    -100 if failure 4
    """
    def calculate_new_health(self, current_health, number_failures, success):
        if success: 
            return current_health + 25
        return current_health - 25
        """
        if success:
            return current_health + 25
        elif number_failures == 1:
            return current_health - 25 
        elif number_failures == 2:
            return current_health - 50
        elif number_failures == 3: 
            return current_health - 75
        else:
            return current_health - 100
        """

    
    """
    Budget Logic (logic resets everyround, budget carries over): 
    +250 if success 
    +100 if failure #1 
    +200 if failure #2
    +300 if failure #3
    +400 if failure #4
    """
    
    def calculate_new_budget(self, current_budget, number_failures, success): 
        if current_budget < 0:
            return 0 
        if success:
            return current_budget + 450 
        elif number_failures == 1:
            return current_budget + 100 
        elif number_failures == 2:
            return current_budget + 200
        elif number_failures == 3: 
            return current_budget + 300
        else: 
            return current_budget + 400
    
    def generate_failure_hint(self, current_level_attacks, current_defenses, player_budget):
        # 1. Map out which defenses are actually useful for THIS level
        effective_keys = set()
        for attack_id in current_level_attacks:
            attack_data = attacks_dict.get(attack_id)
            if attack_data:
                effective_keys.update(attack_data.defenses)

        # 2. Filter defenses: Must be NOT placed AND within budget
        # We create two lists: one for specific counters, one for general availability
        affordable_defenses = []

        for key, defense_obj in defenses_dict.items():
            if key not in current_defenses and defense_obj.cost <= player_budget:
                if key in effective_keys:
                    affordable_defenses.append(key)

        # 3. Selection Priority
        chosen_key = None
        if affordable_defenses:
            # Best case: Suggest a useful, affordable defense
            chosen_key = random.choice(affordable_defenses)
        
        # 4. Building the Return Strings
        if chosen_key:
            defense_obj = defenses_dict.get(chosen_key)
            hint_title = f"STRATEGIC ADVICE"
            # Using specific headers and better spacing
            hint_body = (
                f"--- RECOMMENDED ADDITIONAL DEFENSE ---\n"
                f"DEFENSE: {defense_obj.story_name.upper()}\n"
                f"COST: ${defense_obj.cost}\n\n"
                f"DESCRIPTION: {defense_obj.story_description}\n\n"
                f"--- CYBERSECURITY CONCEPT ---\n"
                f"MITRE D3FENCE: {defense_obj.name}\n"
                f"DESCRIPTION: {defense_obj.mitre_description}\n\n"
                f"REAL WORLD EXAMPLES:\n"
                f"{defense_obj.real_world_examples}"
            )
        else:
            # Ultimate Fallback: Player is likely out of money or all defenses are placed
            hint_title = "Strategic Planning"
            hint_body = "Try diversifying your defenses to cover more attack vectors."

        return hint_title, hint_body
    
    def generate_victory_message(self, attacks, active_defenses):
        
        # Identify which defenses actually blocked something
        effective_defenses = set()
        attack_details_list = []

        for attack_key in attacks:
            attack_obj = attacks_dict.get(attack_key)
            if attack_obj:
                # Check which defenses blocked THIS specific attack
                blockers = [d for d in active_defenses if d in attack_obj.defenses]
                effective_defenses.update(blockers)
                
                # Store info for the "Thwarted Attacks" section
                attack_details_list.append(
                    f"ATTACK: {attack_obj.story_name} [{attack_obj.name}]\n"
                    f"MITRE TECHNIQUE: {attack_obj.name}\n"
                    f"DESCRIPTION: {attack_obj.mitre_description}\n" 
                    f"REAL WORLD EXAMPLES: {attack_obj.real_world_examples}\n" 
                )
        
        # Identify which defenses did not help
        redundant_defenses = [d for d in active_defenses if d not in effective_defenses]

        title = "Mission Debrief: Strategic Victory"

        # Attacks Encountered 
        body = "--- ATTACK ANALYSIS ---\n"
        body += "\n".join(attack_details_list) + "\n"

        if effective_defenses:
            body += "\n--- CYBERSECURITY CONCEPTS ---\n"
            for d_key in effective_defenses:
                d_obj = defenses_dict[d_key]
                # Mapping the story name to the professional MITRE technical description
                body += f"DEFENSE: {d_obj.story_name.upper()}\n"
                body += f"MITRE TECHNIQUE: {d_obj.name}\n"
                body += f"DESCRIPTION: {d_obj.mitre_description}\n"
                body += f"REAL WORLD EXAMPLES: {d_obj.real_world_examples}\n\n"
        else:
            body += "STATUS: NO MATCHING DEFENSES\n"
            body += "Result: Tanked via system integrity.\n"

        redundant_defenses = [d for d in active_defenses if d not in effective_defenses]
        if redundant_defenses:
            body += "--- BUDGET ANALYSIS ---\n"
            names = [defenses_dict[d].story_name for d in redundant_defenses]
            body += "UNNECESSARY DEFENSES:\n"
            for d_key in redundant_defenses:
                d_obj = defenses_dict[d_key]
                body += f" • {d_obj.story_name} ({d_obj.name})\n"
            body += "Advice: In high-security environments, maintaining idle defenses increases the 'Attack Surface' and wastes budget that could be used for recovery."
        else:
            body += "EFFICIENCY: 100% - All assets were vital to the defense."

        return title, body

    def generate_game_over_message(self, attacks, active_defenses):
        # Identify which attacks were NOT blocked (the ones that caused the loss)
        unblocked_attacks = []
        attack_details_list = []
        
        for attack_key in attacks:
            attack_obj = attacks_dict.get(attack_key)
            if attack_obj:
                # Check if any of our active defenses were capable of blocking this
                blockers = [d for d in active_defenses if d in attack_obj.defenses]
                
                # If no active defense matches this attack's requirements, it's a breach
                if not blockers:
                    unblocked_attacks.append(attack_obj)
                    attack_details_list.append(
                        f"CRITICAL BREACH: {attack_obj.story_name} [{attack_obj.name}]\n"
                        f"VULNERABILITY: No active mitigation for {attack_obj.name}.\n"
                        f"MITRE DESCRIPTION: {attack_obj.mitre_description}\n"
                        f"REAL WORLD IMPACT: {attack_obj.real_world_examples}\n"
                    )

        title = "Incident Report: System Compromise"

        # Post-Mortem Analysis
        body = "--- ROOT CAUSE ANALYSIS ---\n"
        if attack_details_list:
            body += "\n".join(attack_details_list) + "\n"
        else:
            # Fallback if the loss logic is external to the attack list
            body += "STATUS: System integrity collapsed under sustained pressure.\n"

        # Gaps in Defense
        body += "--- DEFENSE POST-MORTEM ---\n"
        if active_defenses:
            body += "ACTIVE AT TIME OF FAILURE:\n"
            for d_key in active_defenses:
                d_obj = defenses_dict[d_key]
                body += f" • {d_obj.story_name} (Inactive against current threat vector)\n"
        else:
            body += "WARNING: No active defenses were deployed at the time of breach.\n"

        body += "\n--- ADVISORY ---\n"
        body += ("Security is a cat-and-mouse game. The adversary exploited a gap in your "
                "coverage. Review the MITRE techniques above to better align your budget "
                "with the observed threat landscape in the next cycle.")

        return title, body