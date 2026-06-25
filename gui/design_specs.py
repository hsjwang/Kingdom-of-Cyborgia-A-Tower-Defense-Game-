'''
Constants like screen res, fonts, rect sizes, animtation timings
'''
import os
import pygame

from pathlib import Path
import sys

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
    "transitionbutton": pygame.font.Font(resource_path("fonts", "freesansbold.ttf"), 28),
    "title": pygame.font.Font(resource_path("fonts", "freesansbold.ttf"), 22),
    "home_title": pygame.font.Font(resource_path("fonts", "freesansbold.ttf"), 45),
    "end_title": pygame.font.Font(resource_path("fonts", "freesansbold.ttf"), 40),
    "subtitle": pygame.font.Font(resource_path("fonts", "freesansbold.ttf"), 45),
    "budget": pygame.font.SysFont("courier new", 33, bold=True),  
    "health": pygame.font.Font(resource_path("fonts", "freesansbold.ttf"), 35),
    "small": pygame.font.Font(resource_path("fonts", "freesansbold.ttf"), 16),
    "end_desc": pygame.font.Font(resource_path("fonts", "freesansbold.ttf"), 23),
    "dfont": pygame.font.Font(resource_path("fonts", "freesansbold.ttf"), 14),
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
    "hints": pygame.font.Font(resource_path(os.path.join("fonts", "freesansbold.ttf")), 21)
}

FONTS["header"].set_bold(True)
FONTS["btn_font_21"].set_bold(True)
FONTS["lock_font"].set_bold(True)
FONTS["btn_font_24"].set_bold(True)
FONTS["label_font"].set_bold(True)
FONTS["phase"].set_bold(True)
FONTS["guide"].set_bold(True)


ATTACK_FILES = {
    "T1566": "T1566.png",
    "T1552": "T1552.png",
    "T1098": "T1098.png",
    "T1027": "T1027.png",
    "T1059": "T1059.png",
    # "T1055": "T1055.png",
}

CASTLE_SOCKETS = {
    "AV": (815, 300),            # Top of front left tower
    "Audit": (965, 300),         # Top of front right tower
    "WebRestrict": (900, 500),   # Front gate
    "Training": (580, 300),  # Top of middle left tower
    "OSConfig": (660, 470),      # Left front wall
    "PAM": (1150, 550),           # Walkway to front gate in front of people
    "RestrictPerms": (700, 170),   # Top of tower
    "MFA": (710, 280),           # Font of top tower (middle above glowing bit)
    "DataBackup": (520, 240),    # Top left of tower
    "RemoteData": (1200, 450), # Left far back behind castle
    "SSLInspect": (1000, 540)     # Middle of bridge behind PAM, infront of gates
}


# --- How to play data for the guide pages --- 
HOW_TO_PLAY_DATA = [
    {
        "title": "Welcome to the Kingdom of Cyborgia, located on a server far far away.....",
        "description": "The Shadow Guild is at our borders. As the newly appointed Castellan, your job is to allocate the King’s Gold to build the right defenses. You have a limited budget each round—choose wisely. Once a defense is built, it remains part of your castle, but every turn the Guild will try a new, more devious tactic."
    },
    {
        "title": "Build Phase",
        "description": "You can view the incoming attacks by clicking on the Intel Report button. Defenses are available in the cabinet, with your allocated budget on top. Drag the selected defense to its correpsonding location on the game board to purchase it. Once the defenses are placed, they can't be moved. When you are ready, click LOCK DEFENCES to begin the attack."
    },
    {
        "title": "Attack Phase",
        "description": "Once defenses are locked, the attacker launches threats against your castle. If chosen correctly, your placed defenses help block attacks and protect your health. If chosen incorrectly, you will lose health and have to repeat the level."
    },
    {
        "title": "Winning and Losing",
        "description": "There are three total levels. Survive each round to move to the next level. If your health reaches zero, the castle falls and the game ends. You can earn additional shield health by successfully passing levels."
    }
]

# --- Defense metadata for the guidebook --- 
DEFENSE_GUI_PAGES = [
    {
        "title": "The Kennel Hounds",
        "description": "Trained beasts that sniff out poisoned items, hidden daggers, or any 'unnatural' objects brought into the keep.",
        "image": os.path.join("images", "av.png")
    },
    {
        "title": "The Scribe’s Ledger",
        "description": "A meticulous monk sits by the gate and records every single soul who enters, leaves, or moves between rooms. It doesn't stop a crime, but it tells you exactly who did it.",
        "image": os.path.join("images", "audit.png")
    },
    {
        "title": "The Scribe's Vault",
        "description": "Keeps reserve copies of the kingdom's records so losses can be restored after an attack.",
        "image": os.path.join("images", "databackup.png")
    },
    {
        "title": "The Portcullis Toll:",
        "description": "A checkpoint at the edge of the kingdom that stops merchants from known 'enemy lands' and bans the entry of strange, unknown crates.",
        "image": os.path.join("images", "webrestrict.png")
    },
    {
        "title": "The Village Drills:",
        "description": "Regular town halls where peasants are taught that 'The King' will never ask for their gold coins via a random messenger bird.",
        "image": os.path.join("images", "training.png")
    },
    {
        "title": "Stone Wall Reinforcement:",
        "description": "Laborers fill in old cracks, seal unused drainage pipes, and remove hidden 'thief holes' in the masonry.",
        "image": os.path.join("images", "osconfig.png")
    },
    {
        "title": "The Outland Post",
        "description": "Stores copies far from the castle so a local disaster cannot destroy everything at once.",
        "image": os.path.join("images", "remotedata.png")
    },
    {
        "title": "The Royal Guard:",
        "description": "Elite soldiers who shadow high- ranking officials. They ensure only the most trusted hands touch the Royal Scepter.",
        "image": os.path.join("images", "pam.png")
    },
    {
        "title": "Iron-Bound Chests:",
        "description": "Sensitive documents are locked in specific rooms. A cook doesn't need the key to the armory, and a stablehand doesn't need the key to the treasury.",
        "image": os.path.join("images", "restrictperms.png")
    },
    {
        "title": "The Royal Inquisitor",
        "description": "Examines sealed deliveries for hidden dangers before allowing them into the keep.",
        "image": os.path.join("images", "sslinspect.png")
    },
    {
        "title": "The Two-Key Vault:",
        "description": "Requires a physical seal and a secret whisper. Even if a guard's keys are stolen, the vault stays shut.",
        "image": os.path.join("images", "mfa.png")
    }
]

VISIBLE_DEFENSES = [
    "AV",
    "Audit",
    "DataBackup",
    "WebRestrict",
    "Training",
    "OSConfig",
    "RemoteData",
    "PAM",
    "RestrictPerms",
    "SSLInspect",
    "MFA",
]

NARRATIVE_NAMES = {
    "AV": "The Kennel Hounds",
    "Audit": "The Scribe's Ledger",
    "WebRestrict": "The Portcullis Toll",
    "Training": "The Village Drills",
    "OSConfig": "Wall Reinforcement",
    "PAM": "The Royal Guard",
    "RestrictPerms": "Iron-Bound Chests",
    "MFA": "The Two-Key Vault",
    "DataBackup": "The Scribe's Vault",
    "RemoteData": "The Outland Post",
    "SSLInspect": "The Royal Inquisitor"
}

DEFENSE_KEYS = [
    "AV",
    "Audit",
    "DataBackup",
    "WebRestrict",
    "Training",
    "OSConfig",
    "RemoteData",
    "PAM",
    "RestrictPerms",
    "SSLInspect",
    "MFA"
]