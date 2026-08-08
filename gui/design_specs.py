'''
Constants like screen res, fonts, rect sizes, animtation timings
'''
import os
import pygame

from pathlib import Path
import sys
from engine.schema import defenses_dict, attacks_dict

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

def resource_path(*parts) -> str:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent.parent
    return str(base_path.joinpath(*parts))

pygame.font.init()
HEALTH_THRESHOLDS = [25, 50, 75, 100, 125, 150, 175]
SCREEN_RES = (1280, 720)

# SCREEN & LAYOUT 
GRID_SIZE = 80
ICON_SIZE = 20
ATTACK_DURATION = 3000     # 3 seconds of animation before auto-resolving
SCOLL_SPEED = 30
CASTLE_SPACING = 50
VICTORY_DELAY = 120 

# UI COMPONENT DIMENSIONS 
POPUP_W, POPUP_H = 555, 240
GUIDE_X, GUIDE_Y = 300, 650
GUIDE_W, GUIDE_H = 140, 50
TIMER_X, TIMER_Y = 1135, 75
TIMER_W, TIMER_H = 170, 55
DRAGON_W, DRAGON_H = 300, 200
BUDGET_X, BUDGET_Y = 100, 58
PHASE_X, PHASE_Y = 380, 80
BOX_W, BOX_Y = 300, 60

# STATIC RECTS 
FIELD_RECT = pygame.Rect(200, 0, 1080, 720)
NARRATIVE_RECT = pygame.Rect(0, 0, POPUP_W, POPUP_H)
NARRATIVE_RECT.center = (740, 360) 

NARRATIVE_CONTINUE_RECT = pygame.Rect(0, 0, 160, 36)
NARRATIVE_CONTINUE_RECT.centerx = NARRATIVE_RECT.centerx
NARRATIVE_CONTINUE_RECT.bottom = NARRATIVE_RECT.bottom - 11

GUIDE_RECT = pygame.Rect(0, 0, GUIDE_W, GUIDE_H)
GUIDE_RECT.center = (GUIDE_X, GUIDE_Y)

CABINET_VIEW_RECT = pygame.Rect(0, 120, 200, 500)

GUIDEBOOK_RECT = pygame.Rect(300, 60, 680, 580)
CLOSE_RECT = pygame.Rect(840, 150, 50, 40)
BACK_RECT = pygame.Rect(385, 150, 90, 40)

GUIDE_IMAGE_RECT = pygame.Rect(0, 0, 0, 0)
LEFT_PAGE_TURN_RECT = pygame.Rect(350, 560, 60, 40)   # Bottom Left
RIGHT_PAGE_TURN_RECT = pygame.Rect(870, 560, 60, 40)  # Bottom Right

MENU_HOWTO_RECT = pygame.Rect(0, 0, 220, 65)
MENU_DEFENSES_RECT = pygame.Rect(0, 0, 220, 65)
MENU_HOWTO_RECT.center = (GUIDEBOOK_RECT.centerx, GUIDEBOOK_RECT.centery - 60)
MENU_DEFENSES_RECT.center = (GUIDEBOOK_RECT.centerx, GUIDEBOOK_RECT.centery + 30)

TIMER_RECT = pygame.Rect(0, 0, TIMER_W, TIMER_H)
TIMER_RECT.center = (TIMER_X, TIMER_Y)

TRASH_CAN_RECT = pygame.Rect(215, 470, 180, 180) # Example position

# --- UI COLORS ---
COLORS = {
    "blue_sky": (177, 236, 246),
    "green_grass": (108, 247, 91),
    "yellow_startbutton": (250, 246, 4),
    "yellow_startbutton_hover": (201, 199, 49),
    "defense_cabinet": (122, 67, 43),
    "black": (0, 0, 0),
    "cabinet_icons": (255, 255, 255),
    "cabinet_outline": (180, 80, 255),
    "cabinet_icons_hover": (199, 198, 197),
    "panel_dark": (15, 15, 18),
    "panel_shadow": (20, 10, 5),
    "neon_purple": (180, 80, 255),
    "danger_red": (255, 50, 50),
    "money_gold": (255, 215, 0),
}

FONTS = {
    "playbutton": pygame.font.Font(resource_path("fonts", "freesansbold.ttf"), 33),
    "custom_start": pygame.font.Font(resource_path("fonts", "freesansbold.ttf"), 30),
    "transitionbutton": pygame.font.Font(resource_path("fonts", "freesansbold.ttf"), 28),
    "title": pygame.font.Font(resource_path("fonts", "freesansbold.ttf"), 22),
    "home_title": pygame.font.Font(resource_path("fonts", "freesansbold.ttf"), 45),
    "end_title": pygame.font.Font(resource_path("fonts", "freesansbold.ttf"), 40),
    "subtitle": pygame.font.Font(resource_path("fonts", "freesansbold.ttf"), 45),
    "budget": pygame.font.SysFont("courier new", 33, bold=True),  
    "health": pygame.font.Font(resource_path("fonts", "freesansbold.ttf"), 35),
    "small": pygame.font.Font(resource_path("fonts", "freesansbold.ttf"), 16),
    "end_desc": pygame.font.Font(resource_path("fonts", "freesansbold.ttf"), 23),
    "dfont": pygame.font.Font(resource_path("fonts", "freesansbold.ttf"), 15),
    "level": pygame.font.Font(resource_path("fonts", "freesansbold.ttf"), 27),
    "xwindow": pygame.font.SysFont("arial", 30),  
    "guide_text": pygame.font.SysFont("georgia", 20),  
    "intel_desc": pygame.font.Font(resource_path("fonts", "freesansbold.ttf"), 15),
    "hint_desc": pygame.font.Font(resource_path("fonts", "freesansbold.ttf"), 16),
    "def_keep": pygame.font.Font(resource_path("fonts", "freesansbold.ttf"), 18),
    "header":  pygame.font.Font(resource_path(os.path.join("fonts", "freesansbold.ttf")), 25),
    "btn_font_21": pygame.font.Font(resource_path(os.path.join("fonts", "freesansbold.ttf")), 19),
    "lock_font": pygame.font.Font(resource_path(os.path.join("fonts", "freesansbold.ttf")), 15),
    "btn_font_24": pygame.font.Font(resource_path(os.path.join("fonts", "freesansbold.ttf")), 24),
    "label_font": pygame.font.Font(resource_path(os.path.join("fonts", "freesansbold.ttf")), 16),
    "phase": pygame.font.Font(resource_path(os.path.join("fonts", "freesansbold.ttf")), 25),
    "guide": pygame.font.Font(resource_path(os.path.join("fonts", "freesansbold.ttf")), 22),
    "hints": pygame.font.Font(resource_path(os.path.join("fonts", "freesansbold.ttf")), 21),
}

FONTS["header"].set_bold(True)
FONTS["btn_font_21"].set_bold(True)
FONTS["lock_font"].set_bold(True)
FONTS["btn_font_24"].set_bold(True)
FONTS["label_font"].set_bold(True)
FONTS["phase"].set_bold(True)
FONTS["guide"].set_bold(True)


ATTACK_FILES = {attack_id: f"{attack_id}.png" for attack_id in attacks_dict}


#button.py
CASTLE_SOCKETS = {
    "M1049": (815, 300),            # Top of front left tower
    "M1047": (965, 300),         # Top of front right tower
    "M1021": (900, 500),   # Front gate
    "M1017": (580, 300),  # Top of middle left tower
    "M1028": (660, 470),      # Left front wall
    "M1026": (1150, 550),           # Walkway to front gate in front of people
    "M1022": (700, 170),   # Top of tower
    "M1032": (710, 280),           # Font of top tower (middle above glowing bit)
    "M1053": (520, 240),    # Top left of tower
    "M1029": (1200, 450), # Left far back behind castle
    "M1020": (1000, 540),     # Middle of bridge behind PAM, infront of gates
    "M1015": (1200, 200), 
    "M1018": (1200, 550), 
    "M1027": (800, 600), 
    "M1030": (350, 390), 
    "M1031": (800, 200), 
    "M1033": (260, 380), 
    "M1035": (700, 600), 
    "M1037": (1050, 440), 
    "M1038": (880, 380), 
    "M1040": (1100, 260), 
    "M1041": (900, 300), 
    "M1042": (520, 550), 
    "M1045": (650, 350), 
    "M1051": (480, 410), 
    "M1054": (440, 300) # regen
}

# visible defenses in beginner mode 
VISIBLE_DEFENSES = [
    "M1049",
    "M1047",
    "M1053",
    "M1021",
    "M1026",
    "M1017",
    "M1028",
    "M1029",
    "M1032",
    "M1022",
    "M1020"
]

DEFENSE_GUI_PAGES = []

for key, defense in defenses_dict.items():
    image_filename = f"{defense.id}.png" 
    image_path = os.path.join("images", image_filename)

    # Missing images are handled by Loader with a placeholder.
    page_data = {
        "defense_key": key,
        "title": defense.story_name,
        "description": defense.story_description,
        "image": image_path,
    }
    DEFENSE_GUI_PAGES.append(page_data)
