'''
Handles the state of the game (variables and reset functionality)
'''
import pygame 
from gui.button import createDefenseButtons
import gui.design_specs as gs

class UIState:
    def __init__(self):
        self.game_state = "Title Screen"
        
        # Animations & Timers
        self.sim_timer = 0
        self.attack_auto_timer = 0
        self.shake_amount = 0
        self.scroll_y = 0
        self.max_scroll = 0
        self.frame = 0
        self.victory_timer = 0
        self.shield_scale = 0.0
        self.dragon_pos = pygame.Vector2(-200, 150)
        
        # Logic Flags
        self.feedback_title = ""
        self.feedback_body = ""
        self.feedback_generated = False
        self.last_seen_level = 0
        
        # Popups
        self.showing_narrative = False
        self.narrative_index = 0
        self.show_guidebook = False
        self.guidebook_page = 0
        self.guidebook_section = "menu"

        self.narrative_opened_for_level = False

        self.showing_feedback = False
        self.feedback_scroll_y = 0
        self.max_feedback_scroll = 10000

    ### Reset Functions ### 
    def reset_dragon_simulation(self, fire_list):
        """Resets the attack animation sequence."""
        self.sim_timer = 0
        fire_list.clear()
        self.dragon_pos = pygame.Vector2(-400, 150)

    def reset_win_animation(self, particles):
        """Resets the victory shield and particle effects."""
        self.shield_scale = 0.0
        self.frame = 0
        self.victory_timer = 0 
        particles.clear() # Use .clear() instead of reassigning [] to keep the reference

    def reset_game(self, server, defense_buttons, fire_list, particles, assets, castle_spacing, info_buttons):
        """Full system reset to initial Title Screen state."""
        server.reset_server()
        
        # Rebuild the dynamic defense buttons
        defense_buttons.clear()
        info_buttons.clear()
        createDefenseButtons(defense_buttons, server, castle_spacing, info_buttons, assets.defense_images)
        
        # Internal state resets
        self.show_guidebook = False
        self.game_state = "Title Screen"
        self.guidebook_section = "menu"
        self.guidebook_page = 0

        self.feedback_title = ""
        self.feedback_body = ""
        self.feedback_generated = False

        self.max_scroll = 0
        self.scroll_y = 0

        self.last_seen_level = 0

        self.showing_feedback = False
        self.feedback_scroll_y = 0
        self.max_feedback_scroll = 10000
        
        self.reset_dragon_simulation(fire_list)
        self.reset_win_animation(particles)
        
        print("[SYSTEM] Game Reset Successful.")
        return defense_buttons, info_buttons