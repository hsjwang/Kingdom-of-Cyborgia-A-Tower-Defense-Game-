'''
Handles Loading and Scaleing of Images 
'''
import pygame
import os
from gui.design_specs import resource_path, SCREEN_RES, ATTACK_FILES, HEALTH_THRESHOLDS, ICON_SIZE, DRAGON_W, DRAGON_H, DEFENSE_GUI_PAGES, GUIDEBOOK_RECT
from engine.schema import defenses_dict, HOW_TO_PLAY_DATA

class Loader:
    def __init__(self):
        self.defense_images = {}
        self.attack_images = {}
        self.backgrounds = {}
        self.dragon_img = None 
        self.shield_img = None
        self.health_icon = None
        self.shield_icon = None
        self.guidebook_bg = None
        self.current_bg = None
        self.trash_can_img = None
        self.load_all_assets()

    def load_defense_image(self, filename, size=(100, 100)):
        image = pygame.image.load(resource_path(os.path.join("images", filename))).convert_alpha()
        return pygame.transform.scale(image, size)
    
    def get_current_bg(self,health):
        # We check the list in REVERSE (175, 150, 125...) 
        # The first one that is <= health is our current background.
        for threshold in reversed(HEALTH_THRESHOLDS):
            if health >= threshold:
                return self.backgrounds[threshold]

        # 3. Absolute fallback
        return self.backgrounds[25]

    def load_all_assets(self):
        # Backgrounds
        self.backgrounds = {
            lvl: pygame.transform.scale(
                pygame.image.load(resource_path(os.path.join("images", f"{lvl}HealthLandscape.png"))).convert(),
                SCREEN_RES
            ) for lvl in [25, 50, 75, 100, 125, 150, 175]
        }
        
        # Attacks
        for attack_id, filename in ATTACK_FILES.items():
            img = pygame.image.load(resource_path(os.path.join("images", filename))).convert_alpha()
            self.attack_images[attack_id] = pygame.transform.scale(img, (90, 90))
        
        # Defenses
        for key in defenses_dict:
            filename = f"{key.lower()}.png"
            path = resource_path(os.path.join("images", filename))
            
            if os.path.exists(path):
                # FIXED: Removed 'self' from the arguments
                self.defense_images[key] = self.load_defense_image(filename)
            else:
                print(f"[GUI WARNING] Could not find image: {path}. Using placeholder.")
        
        # Guidebook 
        self.guidebook_bg = pygame.image.load(resource_path(os.path.join("images", "guidebook_bg.png"))).convert_alpha()
        self.guidebook_bg = pygame.transform.smoothscale(self.guidebook_bg, (GUIDEBOOK_RECT.width, GUIDEBOOK_RECT.height))

        for page in DEFENSE_GUI_PAGES:
            if page["image"] is not None:
                page_img = pygame.image.load(resource_path(page["image"])).convert_alpha()
                page["loaded_image"] = pygame.transform.smoothscale(page_img, (180, 180))
            else:
                page["loaded_image"] = None

        for page in HOW_TO_PLAY_DATA:
            page["loaded_image"] = None

        #Add health and shield icons
        self.health_icon = pygame.image.load(resource_path(os.path.join("images", "health_icon.png"))).convert_alpha()
        self.shield_icon = pygame.image.load(resource_path(os.path.join("images", "shield_icon.png"))).convert_alpha()
        self.health_icon = pygame.transform.scale(self.health_icon, (ICON_SIZE, ICON_SIZE))
        self.shield_icon = pygame.transform.scale(self.shield_icon, (ICON_SIZE, ICON_SIZE))

        # End of Game Loss Variables (Dragon) 
        original_dragon = pygame.image.load(resource_path(os.path.join("images", "losing_dragon.png"))).convert_alpha()
        self.dragon_img = pygame.transform.scale(original_dragon, (DRAGON_W, DRAGON_H))

        # Shield 
        self.shield_img = pygame.image.load(resource_path(os.path.join("images", "winning_shield.png"))).convert_alpha()

        self.trash_can_img = pygame.image.load(resource_path(os.path.join("images", "trash_can.png"))).convert_alpha()
