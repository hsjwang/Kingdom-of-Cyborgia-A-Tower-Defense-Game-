'''
Handles Loading and Scaleing of Images 
'''
import pygame
import os
from gui.design_specs import resource_path, SCREEN_RES, ATTACK_FILES, HEALTH_THRESHOLDS, ICON_SIZE, DRAGON_W, DRAGON_H, DEFENSE_GUI_PAGES, GUIDEBOOK_RECT, VISIBLE_DEFENSES
from engine.schema import defenses_dict, attacks_dict, HOW_TO_PLAY_DATA

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

    def load_defense_image(self, filename, size=(90, 90)):
        # Attempt to load the asset normally
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
        
        placeholder_path = resource_path(os.path.join("images", "trash_can.png"))
        placeholder = pygame.image.load(placeholder_path).convert_alpha()

        # Load every attack in the schema so Random mode can use newly added attacks.
        for attack_id in attacks_dict:
            filename = ATTACK_FILES.get(attack_id, f"{attack_id}.png")
            path = resource_path(os.path.join("images", filename))
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
            else:
                img = placeholder.copy()
                print(f"[GUI WARNING] Could not find attack image: {path}. Using placeholder.")
            self.attack_images[attack_id] = pygame.transform.scale(img, (90, 90))

        # Load every defense in the schema. The server decides which ones appear.
        for key in defenses_dict:
            filename = f"{key}.png"
            path = resource_path(os.path.join("images", filename))
            if os.path.exists(path):
                self.defense_images[key] = self.load_defense_image(filename)
            else:
                self.defense_images[key] = pygame.transform.scale(placeholder.copy(), (80, 80))
                print(f"[GUI WARNING] Could not find defense image: {path}. Using placeholder.")
            
        # Guidebook 
        self.guidebook_bg = pygame.image.load(resource_path(os.path.join("images", "guidebook_bg.png"))).convert_alpha()
        self.guidebook_bg = pygame.transform.smoothscale(self.guidebook_bg, (GUIDEBOOK_RECT.width, GUIDEBOOK_RECT.height))

        for page in DEFENSE_GUI_PAGES:
            page_path = resource_path(page["image"]) if page.get("image") else None
            if page_path and os.path.exists(page_path):
                page_img = pygame.image.load(page_path).convert_alpha()
            else:
                page_img = placeholder.copy()
            page["loaded_image"] = pygame.transform.smoothscale(page_img, (180, 180))

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
