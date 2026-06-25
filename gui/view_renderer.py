'''
Drawing Functions for the GUI
'''
import pygame
import math
import random
from gui.design_specs import COLORS, FONTS
import gui.design_specs as gs
from engine.schema import attacks_dict
from gui.fire_particle import FireParticle

### Drawing Functions ###
def draw_wrapped_text(surface, text, color, rect, font, line_spacing=0):
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= rect.width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)

    # Calculate total height
    total_height = len(lines) * (font.get_height() + line_spacing)

    # Start Y so text is vertically centered
    y = rect.y + (rect.height - total_height) // 2

    for line in lines:
        line_surface = font.render(line.strip(), True, color)
        line_rect = line_surface.get_rect(center=(rect.centerx, y + line_surface.get_height() // 2))
        surface.blit(line_surface, line_rect)

        y += font.get_height() + line_spacing

def draw_guidebook(screen, ui_state, loader):

    mouse = pygame.mouse.get_pos()

    overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 140))
    screen.blit(overlay, (0, 0))

    screen.blit(loader.guidebook_bg, gs.GUIDEBOOK_RECT.topleft)

    # Close button
    close_color = (100, 60, 30) if gs.CLOSE_RECT.collidepoint(mouse) else (70, 40, 20)
    pygame.draw.rect(screen, close_color, gs.CLOSE_RECT, border_radius=8)
    pygame.draw.rect(screen, COLORS["black"], gs.CLOSE_RECT, width=2, border_radius=8)
    close_surface = FONTS["xwindow"].render("X", True, (255, 240, 220))
    close_text_rect = close_surface.get_rect(center=gs.CLOSE_RECT.center)
    screen.blit(close_surface, close_text_rect)

    # Back button on non-menu pages
    if ui_state.guidebook_section != "menu":
        back_color = (100, 60, 30) if gs.BACK_RECT.collidepoint(mouse) else (70, 40, 20)
        pygame.draw.rect(screen, back_color, gs.BACK_RECT, border_radius=8)
        pygame.draw.rect(screen, COLORS["black"], gs.BACK_RECT, width=2, border_radius=8)
        back_surface = FONTS["small"].render("BACK", True, (255, 240, 220))
        back_text_rect = back_surface.get_rect(center=gs.BACK_RECT.center)
        screen.blit(back_surface, back_text_rect)

    # Main menu page
    if ui_state.guidebook_section == "menu":
        menu_font = pygame.font.SysFont("georgia", 36, bold=True)
        menu_font_button = pygame.font.SysFont("georgia", 21, bold=True)
        body_font = FONTS["guide_text"]

        subtitle = menu_font.render("Guidebook", True, (50, 28, 10))
        subtitle_rect = subtitle.get_rect(center=(gs.GUIDEBOOK_RECT.centerx, gs.GUIDEBOOK_RECT.top + 150))
        screen.blit(subtitle, subtitle_rect)
        mouse = pygame.mouse.get_pos()

        howto_color = (100, 60, 30) if gs.MENU_HOWTO_RECT.collidepoint(mouse) else (70, 40, 20)
        pygame.draw.rect(screen, howto_color, gs.MENU_HOWTO_RECT, border_radius=10)
        pygame.draw.rect(screen, COLORS["black"], gs.MENU_HOWTO_RECT, width=2, border_radius=10)
        howto_text = menu_font_button.render("How to Play", True, (255, 240, 220))
     
        howto_text_rect = howto_text.get_rect(center=gs.MENU_HOWTO_RECT.center)
        screen.blit(howto_text, howto_text_rect)
        def_color = (100, 60, 30) if gs.MENU_DEFENSES_RECT.collidepoint(mouse) else (70, 40, 20)
        pygame.draw.rect(screen, def_color, gs.MENU_DEFENSES_RECT, border_radius=10)
        pygame.draw.rect(screen, COLORS["black"], gs.MENU_DEFENSES_RECT, width=2, border_radius=10)
        defenses_text = menu_font_button.render("Defenses", True, (255, 240, 220))
        defenses_text_rect = defenses_text.get_rect(center=gs.MENU_DEFENSES_RECT.center)
        screen.blit(defenses_text, defenses_text_rect)

        info_rect = pygame.Rect(
            gs.GUIDEBOOK_RECT.left + 110,
            gs.GUIDEBOOK_RECT.top + 370,
            gs.GUIDEBOOK_RECT.width - 220,
            90
        )
        draw_wrapped_text(
            screen,
            "Select a section to learn the rules of the game or browse the kingdom's defenses.",
            (45, 25, 10),
            info_rect,
            body_font,
            line_spacing=6
        )

        gs.GUIDE_IMAGE_RECT = pygame.Rect(0, 0, 0, 0)
        gs.LEFT_PAGE_TURN_RECT = pygame.Rect(0, 0, 0, 0)
        gs.RIGHT_PAGE_TURN_RECT = pygame.Rect(0, 0, 0, 0)
        return

    # Pick which page list to use
    if ui_state.guidebook_section == "how_to_play":
        current_pages = gs.HOW_TO_PLAY_DATA
    else:
        current_pages = gs.DEFENSE_GUI_PAGES

    current_page = current_pages[ui_state.guidebook_page]

    # ---------- IMAGE + PAGE TURN AREAS ----------
    if ui_state.guidebook_section == "defenses":
        gs.GUIDE_IMAGE_RECT = pygame.Rect(
            gs.GUIDEBOOK_RECT.centerx - 90,
            gs.GUIDEBOOK_RECT.top + 100,
            180,
            180
        )

        if current_page["loaded_image"] is not None:
            screen.blit(current_page["loaded_image"], gs.GUIDE_IMAGE_RECT)

        gs.LEFT_PAGE_TURN_RECT = pygame.Rect(
          gs.GUIDEBOOK_RECT.left + 25,
          gs.GUIDEBOOK_RECT.top + 260,
          40,
          70
        )
        gs.RIGHT_PAGE_TURN_RECT = pygame.Rect(
          gs.GUIDEBOOK_RECT.right - 70,
          gs.GUIDEBOOK_RECT.top + 260,
          40,
          70
        )
    else:
        # No image for How to Play pages
        gs.GUIDE_IMAGE_RECT= pygame.Rect(0, 0, 0, 0)

        # Put page turn zones near the upper left/right sides of the book
        gs.LEFT_PAGE_TURN_RECT = pygame.Rect(
            gs.GUIDEBOOK_RECT.left + 25,
            gs.GUIDEBOOK_RECT.top + 260,
            40,
            70
        )
        gs.RIGHT_PAGE_TURN_RECT = pygame.Rect(
            gs.GUIDEBOOK_RECT.right - 70,
            gs.GUIDEBOOK_RECT.top + 260,
            40,
            70
        )

    # Draw page turn arrows
    arrow_font = pygame.font.SysFont("georgia", 34, bold=True)

    if ui_state.guidebook_page > 0:
        left_arrow = arrow_font.render("<", True, (80, 45, 20))
        left_arrow_rect = left_arrow.get_rect(center=gs.LEFT_PAGE_TURN_RECT.center)
        screen.blit(left_arrow, left_arrow_rect)

    if ui_state.guidebook_page < len(current_pages) - 1:
        right_arrow = arrow_font.render(">", True, (80, 45, 20))
        right_arrow_rect = right_arrow.get_rect(center=gs.RIGHT_PAGE_TURN_RECT.center)
        screen.blit(right_arrow, right_arrow_rect)

    # ---------- TEXT POSITIONS ----------
    page_title_font = pygame.font.SysFont("georgia", 24, bold=True)

    if ui_state.guidebook_section == "defenses":
        title_rect = pygame.Rect(
            gs.GUIDEBOOK_RECT.left + 90,
            gs.GUIDEBOOK_RECT.top + 295,
            gs.GUIDEBOOK_RECT.width - 180,
            45
        )

        desc_rect = pygame.Rect(
            gs.GUIDEBOOK_RECT.left + 90,
            gs.GUIDEBOOK_RECT.top + 325,
            gs.GUIDEBOOK_RECT.width - 180,
            155
        )

    else:
        # Higher and wider text layout for How to Play
        title_rect = pygame.Rect(
            gs.GUIDEBOOK_RECT.left + 70,
            gs.GUIDEBOOK_RECT.top + 155,
            gs.GUIDEBOOK_RECT.width - 140,
            70
        )

        desc_rect = pygame.Rect(
            gs.GUIDEBOOK_RECT.left + 79,
            gs.GUIDEBOOK_RECT.top + 230,
            gs.GUIDEBOOK_RECT.width - 157,
            220
        )

    draw_wrapped_text(
      screen,
      current_page["title"],
      (45, 25, 10),
      title_rect,
      page_title_font,
      line_spacing=2
    )

    draw_wrapped_text(
        screen,
        current_page["description"],
        (35, 20, 10),
        desc_rect,
        FONTS["guide_text"],
        line_spacing=6
    )

    section_name = "How to Play" if ui_state.guidebook_section == "how_to_play" else "Defenses"
    section_surface = FONTS["small"].render(section_name, True, (60, 35, 10))
    section_rect = section_surface.get_rect(center=(gs.GUIDEBOOK_RECT.centerx, gs.GUIDEBOOK_RECT.bottom - 55))
    screen.blit(section_surface, section_rect)

def draw_narrative_popup(screen, ui_state, current_level_attacks, loader):
    if not ui_state.showing_narrative:
        return

    # 1. Darken the castle field
    overlay = pygame.Surface((1080, 720), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (200, 0))

    # 2. Main Popup Container
    pygame.draw.rect(screen, (20, 20, 25), gs.NARRATIVE_RECT, border_radius=10)
    pygame.draw.rect(screen, COLORS["neon_purple"], gs.NARRATIVE_RECT, width=2, border_radius=10)

    # 3. Get Current Attack Data
    attack_id = current_level_attacks[ui_state.narrative_index]
    attack = attacks_dict[attack_id]

    label = "INTEL REPORT"

    header_shadow = FONTS["header"].render(label, True, (120, 20, 20))  # red shadow to match theme
    header_shadow_rect = header_shadow.get_rect(
        midtop=(gs.NARRATIVE_RECT.centerx + 2, gs.NARRATIVE_RECT.y + 15 + 2)
    )
    screen.blit(header_shadow, header_shadow_rect)

    header_surf = FONTS["header"].render(label, True, COLORS["danger_red"])
    header_rect = header_surf.get_rect(
        midtop=(gs.NARRATIVE_RECT.centerx, gs.NARRATIVE_RECT.y + 15)
    )
    screen.blit(header_surf, header_rect)

    header_surf = FONTS["header"].render(label, True, COLORS["danger_red"])
    header_rect = header_surf.get_rect(
        midtop=(gs.NARRATIVE_RECT.centerx, gs.NARRATIVE_RECT.y + 15)
    )
    screen.blit(header_surf, header_rect)

    # --- IMAGE ---
    if attack_id in loader.attack_images:
        img_size = 110
        large_img = pygame.transform.scale(loader.attack_images[attack_id], (img_size, img_size))
        img_rect = large_img.get_rect(midleft=(gs.NARRATIVE_RECT.x + 40, gs.NARRATIVE_RECT.centery + 3))
        
        border_thickness = 4
        border_rect = img_rect.inflate(border_thickness * 2, border_thickness * 2)
        pygame.draw.rect(screen, COLORS["danger_red"], border_rect, 
                         width=border_thickness, border_radius=10)
        
        screen.blit(large_img, img_rect)

    # --- DESCRIPTION ---
    text_x = gs.NARRATIVE_RECT.x + 185
    desc_height = 120
    desc_rect = pygame.Rect(text_x, 0, 330, desc_height)
    desc_rect.centery = img_rect.centery 
    
    body_font2 = FONTS["intel_desc"]
    narrative_body = getattr(attack, 'story_description', "Scouts report movement at the borders.")
    draw_wrapped_text(screen, narrative_body, (220, 220, 220), 
                      desc_rect, body_font2, line_spacing=4)

    # --- DYNAMIC BUTTON (The Fix) ---
    mouse = pygame.mouse.get_pos()
    is_hover = gs.NARRATIVE_CONTINUE_RECT.collidepoint(mouse)
    btn_color = (30, 30, 35) if is_hover else (20, 20, 20)
    
    pygame.draw.rect(screen, btn_color, gs.NARRATIVE_CONTINUE_RECT, border_radius=5)
    pygame.draw.rect(screen, COLORS["neon_purple"], gs.NARRATIVE_CONTINUE_RECT, width=2, border_radius=5)
    
    label = "CONTINUE" if ui_state.narrative_index < len(current_level_attacks) - 1 else "DEFEND KEEP"
    font = FONTS["def_keep"]

    shadow = font.render(label, True, (100, 40, 150))
    shadow_rect = shadow.get_rect(
        center=(gs.NARRATIVE_CONTINUE_RECT.centerx + 2, gs.NARRATIVE_CONTINUE_RECT.centery + 2)
    )
    screen.blit(shadow, shadow_rect)

    btn_text = font.render(label, True, (180, 80, 255))
    btn_rect = btn_text.get_rect(center=gs.NARRATIVE_CONTINUE_RECT.center)
    screen.blit(btn_text, btn_rect)

def draw_intel_report(screen, state, current_level_attacks, intel_report_btn, gui_state):
    if state != "BUILD_PHASE":
        return

    if current_level_attacks and not gui_state.narrative_opened_for_level:
        pulse_time = pygame.time.get_ticks() / 1000.0
        alpha_factor = (math.sin(pulse_time * 8) + 1) / 2

        glow_inflate = 4 + (6 * alpha_factor)
        glow_rect = intel_report_btn.rect.inflate(glow_inflate, glow_inflate)

        s = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
        glow_color = (255, 50, 50, int(50 + 100 * alpha_factor))
        pygame.draw.rect(
            s,
            glow_color,
            (0, 0, glow_rect.width, glow_rect.height),
            border_radius=12
        )
        screen.blit(s, glow_rect.topleft)

    # always draw the button during build phase
    mouse = pygame.mouse.get_pos()
    is_hover = intel_report_btn.rect.collidepoint(mouse)

    intel_bg = (40, 20, 20) if is_hover else (20, 20, 20)

    pygame.draw.rect(screen, intel_bg, intel_report_btn.rect, border_radius=10)
    pygame.draw.rect(screen, COLORS["danger_red"], intel_report_btn.rect, width=2, border_radius=10)

    intel_text = intel_report_btn.textfont.render(
        intel_report_btn.text, True, COLORS["danger_red"]
    )
    intel_text_rect = intel_text.get_rect(center=intel_report_btn.rect.center)

    intel_shadow = intel_report_btn.textfont.render(
        intel_report_btn.text, True, (120, 20, 20)
    )
    intel_shadow_rect = intel_text_rect.move(2, 2)

    screen.blit(intel_shadow, intel_shadow_rect)
    screen.blit(intel_text, intel_text_rect)

def draw_health_bar(screen, x, y, width, height, health, max_health=100):
    ratio = max(0, min(health / max_health, 1))
    fill_width = int(width * ratio)

    pygame.draw.rect(screen, (40, 40, 40), (x, y, width, height), border_radius=5)

    if ratio > 0.6:
        bar_color = (0, 255, 100)
    elif ratio > 0.3:
        bar_color = (255, 200, 0)
    else:
        bar_color = (255, 50, 50)

    if fill_width > 0:
        pygame.draw.rect(screen, bar_color, (x, y, fill_width, height), border_radius=5)
        pygame.draw.line(screen, (255, 255, 255), (x + 2, y + 2), (x + fill_width - 2, y + 2), 2)

    pygame.draw.rect(screen, (200, 200, 200), (x, y, width, height), width=2, border_radius=5)
  
def draw_shield_bar(screen, x, y, width, height, shield, max_health=100):
    ratio = max(0, min(shield / max_health, 1))
    fill_width = int(width * ratio)

    # gray background always
    pygame.draw.rect(screen, (40, 40, 40), (x, y, width, height), border_radius=5)

    # only draw blue fill if shield > 0
    if fill_width > 0:
        shield_color = (46, 250, 255)
        pygame.draw.rect(screen, shield_color, (x, y, fill_width, height), border_radius=5)
        pygame.draw.line(screen, (255, 255, 255), (x + 2, y + 2), (x + fill_width - 2, y + 2), 2)

    pygame.draw.rect(screen, (200, 200, 200), (x, y, width, height), width=2, border_radius=5)

def split_health_and_shield(total_health):
    if total_health <= 100:
        return total_health, 0
    else:
        return 100, total_health - 100

def draw_game_over(screen, level, player_budget, gui_state, feedback_body):
    # 1. Dark Red/Glitch Overlay
    overlay = pygame.Surface((1280, 720))
    overlay.set_alpha(180)
    overlay.fill((20, 0, 0)) # Near black-red for better text contrast
    screen.blit(overlay, (0, 0))

    # 2. Main Headers (Pushed higher to make room for the report)
    title_surf = FONTS["end_title"].render("SYSTEM COMPROMISED", True, (255, 50, 50))
    title_rect = title_surf.get_rect(center=(640, 60))
    
    reason_surf = FONTS["end_desc"].render("CRITICAL BREACH DETECTED - DATA EXFILTRATED", True, (200, 200, 200))
    reason_rect = reason_surf.get_rect(center=(640, 110))

    # 3. The Incident Report Window (The "Debrief")
    # Adjusted to sit comfortably in the middle
    report_rect = pygame.Rect(240, 150, 800, 420)
    # Background: Darker, desaturated red-black
    pygame.draw.rect(screen, (30, 10, 10), report_rect, border_radius=10) 
    # Border: High-alert Red
    pygame.draw.rect(screen, (255, 50, 50), report_rect, width=2, border_radius=10) 

    # --- SCROLLABLE DEBRIEF LOGIC ---
    view_rect = report_rect.inflate(-40, -40) 
    
    # Virtual canvas for the long report
    text_canvas = pygame.Surface((view_rect.width - 30, 4000), pygame.SRCALPHA)
    
    total_height = draw_feedback_text(
        text_canvas, 
        feedback_body, 
        (255, 200, 200), # Light red-tinted text
        pygame.Rect(0, 0, view_rect.width - 30, 4000), 
        FONTS["hint_desc"]
    )

    gui_state.max_feedback_scroll = max(0, total_height - view_rect.height + 20)
    scroll_y = getattr(gui_state, 'feedback_scroll_y', 0)

    # Blit the report content
    screen.set_clip(view_rect)
    screen.blit(text_canvas, (view_rect.x, view_rect.y - scroll_y))
    screen.set_clip(None)

    # 4. Scroll Indicator
    if gui_state.max_feedback_scroll > 0:
        bar_x = view_rect.right + 10
        bar_y = view_rect.y
        bar_h = view_rect.height
        
        pygame.draw.rect(screen, (60, 20, 20), (bar_x, bar_y, 4, bar_h)) # Track
        
        fraction = scroll_y / gui_state.max_feedback_scroll
        thumb_h = 40
        thumb_y = bar_y + (fraction * (bar_h - thumb_h))
        pygame.draw.rect(screen, (255, 50, 50), (bar_x, thumb_y, 4, thumb_h), border_radius=2)

    # 5. Final Stats (Moved below the report)
    stat_text = f"LAST STABLE LEVEL: {level} | TOTAL LOSSES: ${player_budget:,}"
    stat_surf = FONTS["small"].render(stat_text, True, (180, 180, 180))
    stat_rect = stat_surf.get_rect(center=(640, 600))

    # 6. Interaction Prompts
    prompt_surf = FONTS["small"].render("PRESS [ESC] TO REBOOT SYSTEM", True, (255, 50, 50))
    prompt_rect = prompt_surf.get_rect(center=(640, 660))
    
    # Rendering everything to screen
    screen.blit(title_surf, title_rect)
    screen.blit(reason_surf, reason_rect)
    screen.blit(stat_surf, stat_rect)
    screen.blit(prompt_surf, prompt_rect)
    
def draw_victory_screen(screen, feedback_body, gui_state):
    # 1. Matrix/Cyber Green Overlay
    overlay = pygame.Surface((1280, 720))
    overlay.set_alpha(210) # Slightly darker for better text contrast
    overlay.fill((0, 20, 20)) 
    screen.blit(overlay, (0, 0))

    # 2. Main Title (Moved up to make room)
    title_surf = FONTS["home_title"].render("MISSION ACCOMPLISHED", True, (0, 255, 150))
    title_rect = title_surf.get_rect(center=(640, 100))
    screen.blit(title_surf, title_rect)

    # 3. Define the Debrief Window
    # Centered on screen, taking up the middle portion
    report_rect = pygame.Rect(240, 160, 800, 400)
    pygame.draw.rect(screen, (0, 40, 40), report_rect, border_radius=15) # Darker box
    pygame.draw.rect(screen, (0, 255, 150), report_rect, width=2, border_radius=15) # Neon border

    # --- SCROLLABLE DEBRIEF LOGIC ---
    # Viewport for the text (inside the report_rect)
    view_rect = report_rect.inflate(-40, -40) # Add margins
    
    # Create the virtual canvas (ensure width matches view_rect)
    text_canvas = pygame.Surface((view_rect.width - 30, 4000), pygame.SRCALPHA)
    
    # Draw the formatted text onto the canvas
    total_height = draw_feedback_text(
        text_canvas, 
        feedback_body, 
        (220, 255, 240), # Base text color
        pygame.Rect(0, 0, view_rect.width - 30, 4000), 
        FONTS["hint_desc"]
    )

    # Set scroll limits
    gui_state.max_feedback_scroll = max(0, total_height - view_rect.height + 20)

    # Get current scroll from gui_state
    scroll_y = getattr(gui_state, 'feedback_scroll_y', 0)

    # Blit with clipping
    screen.set_clip(view_rect)
    # Important: scroll_y must be subtracted from the Y position
    screen.blit(text_canvas, (view_rect.x, view_rect.y - scroll_y))
    screen.set_clip(None)

    # 4. Scroll Indicator (If content is long)
    if gui_state.max_feedback_scroll > 0:
        indicator_text = "USE SCROLL WHEEL TO READ FULL DEBRIEF"
        ind_surf = FONTS["small"].render(indicator_text, True, (0, 150, 100))

        bar_x = view_rect.right - 10
        bar_y = view_rect.y + 10
        bar_h = view_rect.height - 20
        
        # Track
        pygame.draw.rect(screen, (40, 40, 45), (bar_x, bar_y, 4, bar_h))
        
        # Thumb (the moving part)
        fraction = scroll_y / gui_state.max_feedback_scroll
        thumb_h = 30
        thumb_y = bar_y + (fraction * (bar_h - thumb_h))
        pygame.draw.rect(screen, (220, 255, 240), (bar_x, thumb_y, 4, thumb_h), border_radius=2)

        screen.blit(ind_surf, (report_rect.x, report_rect.bottom + 5))

    # 5. Completion Prompt (Bottom of screen)
    prompt_surf = FONTS["small"].render("PRESS [ESC] TO RETURN TO HQ", True, (0, 255, 150))
    prompt_rect = prompt_surf.get_rect(center=(640, 680))
    screen.blit(prompt_surf, prompt_rect)

def draw_loss_animation(screen, gui_state, fire_list, current_bg, loader,):
    gui_state.sim_timer += 1

    # A. CAMERA SHAKE 
    # Only shake while the dragon is over the main screen area
    gui_state.shake_amount = random.randint(-7, 7) if (100 < gui_state.dragon_pos.x < 1100) else 0

    # B. DRAGON MOVEMENT
    # Move across screen and bob up and down
    gui_state.dragon_pos.x += 6 
    bob_y = math.sin(pygame.time.get_ticks() * 0.005) * 25
    current_dragon_y = gui_state.dragon_pos.y + bob_y

    # C. SPAWN FIRE (The Strafing Run)
    # Adjust +240 and +110 to line up with the head of your dragon image
    if 0 < gui_state.dragon_pos.x < 800:
        for _ in range(6):
            fire_list.append(FireParticle(gui_state.dragon_pos.x + 300, current_dragon_y + 140))

    # D. DRAW WORLD WITH SHAKE
    # Every background and castle element must use (+ shake_amount)
    screen.blit(current_bg, (gui_state.shake_amount + 100, gui_state.shake_amount))
    # castle.draw(screen, offset=shake_amount) # Apply to your castle/towers too!

    # E. UPDATE & DRAW FIRE (Drawn behind the dragon)
    for p in fire_list[:]:
        p.update()
        if p.life <= 0:
            fire_list.remove(p)
        else:
            p.draw(screen)

    # F. DRAW GLOW & DRAGON
    # Fire Glow at the mouth
    glow_size = 250 + random.randint(-20, 20)
    glow_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
    pygame.draw.circle(glow_surf, (255, 100, 0, 50), (glow_size//2, glow_size//2), glow_size//2)
    screen.blit(glow_surf, (gui_state.dragon_pos.x + 240 - glow_size//2, current_dragon_y + 110 - glow_size//2), special_flags=pygame.BLEND_RGBA_ADD)

    # The Dragon Image
    screen.blit(loader.dragon_img, (gui_state.dragon_pos.x, current_dragon_y))

    # G. SEQUENCE END
    # Once dragon is gone and timer is up, switch to Game Over Screen
    if gui_state.sim_timer >= 300:
        print("Castle Destroyed.")
        gui_state.feedback_generated = False
        gui_state.showing_feedback = True

def draw_win_scene(surface, game_state, loader, particles):
    center_x = 690 
    center_y = 360

    if game_state.frame > 0.3:
        if game_state.frame % 4 == 0: # Spawn slightly faster
            import random
            angle = random.uniform(0, 2 * math.pi)
            # Spawn further out (600+ pixels) to cover the 1280 width
            dist = 700 
            px = center_x + math.cos(angle) * dist
            py = center_y + math.sin(angle) * dist
            particles.append([px, py, angle])

        for p in particles[:]:
            p[0] -= math.cos(p[2]) * 10 # Faster inflow
            p[1] -= math.sin(p[2]) * 10
            
            # LARGER PARTICLES: 5x5 squares instead of 3x3
            # Added a slight "trail" by drawing a slightly smaller one behind it
            pygame.draw.rect(surface, (255, 215, 0), (p[0], p[1], 5, 5))
            
            dist_to_center = math.sqrt((p[0]-center_x)**2 + (p[1]-center_y)**2)
            if dist_to_center < 60:
                particles.remove(p)

    if game_state.shield_scale > 0.2:
        # Control the speed with the multiplier (0.05) 
        # Control the max size with the modulo (200)
        ring_progress = (game_state.frame * 3) % 300 
        
        # Calculate transparency: it starts bright and fades as it grows
        ring_alpha = max(0, 150 - (ring_progress // 2))
        
        # Create a surface for the transparent ring
        ring_surf = pygame.Surface((1280, 720), pygame.SRCALPHA)
        
        # Draw the ring (the '2' at the end makes it an outline rather than a solid circle)
        pygame.draw.circle(ring_surf, (255, 215, 0, ring_alpha), (center_x, center_y), ring_progress, 2)
        surface.blit(ring_surf, (0, 0))
    
    # 1. Background "Glow" (keeps pulsing)
    aura_radius = int((120 + game_state.pulse) * game_state.shield_scale)
    aura_surf = pygame.Surface((aura_radius * 2, aura_radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(aura_surf, (255, 215, 0, 80), (aura_radius, aura_radius), aura_radius)
    surface.blit(aura_surf, (center_x - aura_radius, center_y - aura_radius))

    # 2. The Flip Logic
    # We only start flipping once the scale is 1.0 (fully in view)
    flip_width_factor = 1.0
    if game_state.shield_scale >= 0.25:
        # Use a sine wave to go from 1.0 -> 0 -> -1.0 -> 0 -> 1.0
        # Increase the multiplier (0.1) to make the flip faster
        flip_angle = game_state.frame * 0.1 
        flip_width_factor = math.cos(flip_angle)

    # 3. Apply Scaling and Flipping
    # Multiply the width by our flip factor
    SHIELD_WIDTH, SHIELD_HEIGHT = loader.shield_img.get_size()
    scaled_w = int(abs(SHIELD_WIDTH * game_state.shield_scale * flip_width_factor))
    scaled_h = int(SHIELD_HEIGHT * game_state.shield_scale)
    
    # Avoid errors if width hits 0
    if scaled_w < 1: scaled_w = 1
    
    current_shield = pygame.transform.smoothscale(loader.shield_img, (scaled_w, scaled_h))
    
    # If the factor is negative, the shield is "facing away" 
    # (Optional: you could slightly darken the image here for 3D effect)
    if flip_width_factor < 0:
        # This keeps the image from looking "mirrored" if you want a true flip
        current_shield = pygame.transform.flip(current_shield, True, False)

    rect = current_shield.get_rect(center=(center_x, center_y))
    surface.blit(current_shield, rect)

def draw_title_screen(screen, player_health, ui_state, loader, play_button, title_guide_button):
    # 1. Draw the Background (The Castle Image)
        current_bg = loader.get_current_bg(player_health)
        screen.blit(current_bg, (0, 0))

        # 2. Add a semi-transparent "dimmer" so the text is easy to read
        dimmer = pygame.Surface((1280, 720))
        dimmer.set_alpha(100)
        dimmer.fill((0, 0, 0))
        screen.blit(dimmer, (0, 0))

        # 3. Draw the Title
        title_label = "MITRE ATT&CK SIMULATION"
        title_surface = FONTS["home_title"].render(title_label, True, (180, 80, 255))
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, 250))

        title_shadow = FONTS["home_title"].render(title_label, True, (60, 20, 80))
        title_shadow_rect = title_rect.move(2, 2)

        screen.blit(title_shadow, title_shadow_rect)
        screen.blit(title_surface, title_rect)

        # Draw buttons
        mouse = pygame.mouse.get_pos()

        # ---------- PLAY BUTTON ----------
        play_hover = play_button.rect.collidepoint(mouse)
        play_color = (30, 30, 35) if play_hover else (20, 20, 20)

        pygame.draw.rect(screen, play_color, play_button.rect, border_radius=10)
        pygame.draw.rect(screen, COLORS["neon_purple"], play_button.rect, width=2, border_radius=10)

        play_font = play_button.textfont
        play_text = play_font.render(play_button.text, True, COLORS["neon_purple"])
        play_text_rect = play_text.get_rect(center=play_button.rect.center)

        play_shadow = play_font.render(play_button.text, True, (100, 40, 150))
        play_shadow_rect = play_text_rect.move(2, 2)

        screen.blit(play_shadow, play_shadow_rect)
        screen.blit(play_text, play_text_rect)



        # ---------- GUIDE BUTTON ----------
        guide_hover = title_guide_button.rect.collidepoint(mouse)
        guide_color = (30, 30, 35) if guide_hover else (20, 20, 20)

        pygame.draw.rect(screen, guide_color, title_guide_button.rect, border_radius=10)
        pygame.draw.rect(screen, COLORS["neon_purple"], title_guide_button.rect, width=2, border_radius=10)

        guide_font = title_guide_button.textfont
        guide_text = guide_font.render(title_guide_button.text, True, COLORS["neon_purple"])
        guide_text_rect = guide_text.get_rect(center=title_guide_button.rect.center)

        guide_shadow = guide_font.render(title_guide_button.text, True, (100, 40, 150))
        guide_shadow_rect = guide_text_rect.move(2, 2)

        screen.blit(guide_shadow, guide_shadow_rect)
        screen.blit(guide_text, guide_text_rect)

        if ui_state.show_guidebook:
            draw_guidebook(screen, ui_state, loader)

def draw_win_animation(screen, gui_state, loader, particles):
    # 1. Entrance Animation
    if gui_state.shield_scale < 0.25:
        gui_state.shield_scale += 0.001 # Slow and steady growth
    
    gui_state.pulse = math.sin(gui_state.frame * 0.1) * 15
    
    # 2. Draw the scene (your flip logic inside here will now have time to run!)
    draw_win_scene(screen, gui_state, loader, particles)
    gui_state.frame += 1

    # 3. The Delayed "If" Statement
    if gui_state.shield_scale >= 0.25:
        if gui_state.victory_timer < gs.VICTORY_DELAY:
            gui_state.victory_timer += 1
        else:
            # ONLY switch the state once the timer hits the limit
            print("Castle Defended. Transitioning to Victory Screen.")
            gui_state.showing_feedback = True
    
def draw_reset_button(screen, reset_button):
    #Reset button
        reset_button.rect.centery = gs.GUIDE_RECT.centery

        mouse = pygame.mouse.get_pos()

        # --- Align vertically with guide button ---
        reset_button.rect.centery = gs.GUIDE_RECT.centery

        # --- Hover logic ---
        reset_hover = reset_button.rect.collidepoint(mouse)
        reset_color = (30, 30, 35) if reset_hover else (20, 20, 20)

        # --- Draw button ---
        pygame.draw.rect(screen, reset_color, reset_button.rect, border_radius=10)
        pygame.draw.rect(screen, COLORS["neon_purple"], reset_button.rect, width=2, border_radius=10)

        # --- Text + shadow ---
        reset_font = reset_button.textfont

        reset_text = reset_font.render(reset_button.text, True, COLORS["neon_purple"])
        reset_shadow = reset_font.render(reset_button.text, True, (100, 40, 150))

        # perfectly centered
        reset_text_rect = reset_text.get_rect(center=reset_button.rect.center)
        reset_shadow_rect = reset_shadow.get_rect(
            center=(reset_button.rect.centerx + 2, reset_button.rect.centery)
        )

        screen.blit(reset_shadow, reset_shadow_rect)
        screen.blit(reset_text, reset_text_rect)

def draw_attack_sprite(screen, loader, sprite):
    # Calculate movement toward the target castle area
    dx = sprite["target"][0] - sprite["pos"][0]
    dy = sprite["target"][1] - sprite["pos"][1]
    dist = math.hypot(dx, dy)
    
    if dist > 5:
        sprite["pos"][0] += (dx / dist) * sprite["speed"]
        sprite["pos"][1] += (dy / dist) * sprite["speed"]

    # Draw the specific attack icon
    if sprite["id"] in loader.attack_images:
        img = loader.attack_images[sprite["id"]]
        # Add a red "Threat" glow behind the icon for visibility
        glow_surf = pygame.Surface((110, 110), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (255, 50, 50, 100), (55, 55), 45)
        screen.blit(glow_surf, (sprite["pos"][0] - 55, sprite["pos"][1] - 55))
        
        screen.blit(img, img.get_rect(center=sprite["pos"]))
        
        # Fetch the narrative attack name from the schema using story_name
        attack_data = attacks_dict.get(sprite["id"])
        display_name = getattr(attack_data, 'story_name', sprite["id"]) if attack_data else sprite["id"]

        # Label the narrative name under the icon and center it
        name_surf = FONTS["small"].render(display_name, True, (255, 80, 80))
        name_rect = name_surf.get_rect(center=(sprite["pos"][0], sprite["pos"][1] + 65)) 
        screen.blit(name_surf, name_rect)

def draw_budget(screen, player_budget):
    budget_bg_rect = pygame.Rect(0, 0, 160, 60)
    budget_bg_rect.center = (gs.BUDGET_X, gs.BUDGET_Y + 10)
    pygame.draw.rect(screen, (20, 20, 20), budget_bg_rect, border_radius=8)
    pygame.draw.rect(screen, COLORS["money_gold"], budget_bg_rect, width=1, border_radius=8)

    label_surf = FONTS["label_font"].render("AVAILABLE FUNDS", True, COLORS["money_gold"])
    label_rect = label_surf.get_rect(center=(gs.BUDGET_X, gs.BUDGET_Y - 5))
    screen.blit(label_surf, label_rect)


    amount_surf = FONTS["budget"].render(f"${player_budget}", True, (255, 255, 255))
    amount_rect = amount_surf.get_rect(center=(gs.BUDGET_X, gs.BUDGET_Y + 20))
    screen.blit(amount_surf, amount_rect)

def draw_game_titles(screen, level, state):
    # Main title
    shadow_surf = FONTS["title"].render("MITRE ATT&CK SIMULATION", True, (30, 30, 30))
    shadow_rect = shadow_surf.get_rect(center=(744, 34))
    screen.blit(shadow_surf, shadow_rect)

    main_title_surf = FONTS["title"].render("MITRE ATT&CK SIMULATION", True, COLORS["neon_purple"])
    main_title_rect = main_title_surf.get_rect(center=(740, 30))
    screen.blit(main_title_surf, main_title_rect)

    # Level Display
    level_text = f"LEVEL {level}"
    level_shadow_surf = FONTS["level"].render(level_text, True, (20, 20, 20))
    level_shadow_rect = level_shadow_surf.get_rect(center=(742, 77))
    screen.blit(level_shadow_surf, level_shadow_rect)

    level_surf = FONTS["level"].render(level_text, True, (200, 200, 200))
    level_rect = level_surf.get_rect(center=(740, 78))
    screen.blit(level_surf, level_rect)


    # Phase header
    header_rect = pygame.Rect(0, 0, gs.BOX_W, gs.BOX_Y)
    header_rect.center = (gs.PHASE_X, gs.PHASE_Y)

    pygame.draw.rect(screen, (20, 20, 20), header_rect, border_radius=10)
    border_color = COLORS["neon_purple"] if state == "BUILD_PHASE" else COLORS["danger_red"]
    pygame.draw.rect(screen, border_color, header_rect, width=2, border_radius=10)

    phase_text = "BUILD PHASE" if state == "BUILD_PHASE" else "ATTACK PHASE"
    phase_shadow = FONTS["phase"].render(phase_text, True, (100, 40, 150))
    phase_shadow_rect = phase_shadow.get_rect(center=(gs.PHASE_X + 2, gs.PHASE_Y + 2))
    screen.blit(phase_shadow, phase_shadow_rect)

    phase_surf = FONTS["phase"].render(phase_text, True, border_color)
    phase_rect = phase_surf.get_rect(center=(gs.PHASE_X, gs.PHASE_Y))
    screen.blit(phase_surf, phase_rect)

def draw_feedback_text(surface, text, color, rect, font, line_spacing=4):
    lines = text.split('\n')
    x, y = rect.x, rect.y
    line_height = font.size("Tg")[1] + line_spacing
    
    SECTION_COLOR = (180, 100, 255) # Neon Purple for --- SECTION ---
    LABEL_COLOR = (255, 200, 50)    # Gold for KEY:
    
    for line in lines:
        # Detect line types
        is_section = line.startswith("---")
        # We only treat it as a label line if it actually contains a colon
        is_label_line = ":" in line 
        passed_colon = False
        
        words = line.split(' ')
        for word in words:
            # 1. Start with the default body color
            draw_color = color
            
            # 2. Check for Section Highlight (The whole line)
            if is_section:
                draw_color = SECTION_COLOR
            
            # 3. Check for Label Highlight (Before the colon)
            # We explicitly exclude the bullet point symbol from being colored
            elif is_label_line and not passed_colon and word != "•":
                draw_color = LABEL_COLOR
            
            # Update the state if this word contains the colon
            if ":" in word:
                passed_colon = True
                
            word_surface = font.render(word, True, draw_color)
            word_width, _ = word_surface.get_size()
            
            # Word Wrap
            if x + word_width >= rect.right:
                x = rect.x
                y += line_height
            
            surface.blit(word_surface, (x, y))
            x += word_width + font.size(' ')[0]
        
        # Reset for the next line
        x = rect.x
        y += line_height
        
    return y - rect.y
    
def draw_feedback(screen, state, buttons, feedback_title, feedback_body, gui_state):
    # 1. Background Overlay
    overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    # 2. Main Popup Rect
    popup_rect = pygame.Rect(390, 180, 500, 380) 
    pygame.draw.rect(screen, (20, 20, 25), popup_rect, border_radius=15)

    # 3. Define the Scrollable Window (The Viewport)
    view_rect = pygame.Rect(popup_rect.x + 25, popup_rect.y + 80, 450, 210)
    
    if state == "NEXT_LEVEL":
        msg = "MISSION SUCCESS"
        header_color = (80, 255, 150)
        current_popup_btn = buttons["next_level"]
        body_color = (200, 240, 200)
    else:
        msg = "DEFENSES BREACHED"
        header_color = (255, 80, 80)
        current_popup_btn = buttons["retry_level"]
        body_color = (200, 240, 200)        
        

    # --- SCROLLABLE TEXT LOGIC ---
    
    # Create a tall canvas for text. 2000px is usually enough for hints.
    text_canvas = pygame.Surface((view_rect.width, 3000), pygame.SRCALPHA)
    
    # Draw text and CAPTURE the actual height used
    # This height is vital for setting the scroll limit
    total_text_height = draw_feedback_text(
        text_canvas, 
        feedback_body, 
        body_color, 
        pygame.Rect(0, 0, view_rect.width - 30, 2000), 
        FONTS["hint_desc"]
    )

    # Calculate and store the limit so the Event Loop can see it
    # Total text height + padding - the height of the window
    gui_state.max_feedback_scroll = max(0, (total_text_height + 30) - view_rect.height)

    # Get the current scroll position safely
    scroll_y = getattr(gui_state, 'feedback_scroll_y', 0)

    # Blit with Clipping
    screen.set_clip(view_rect)
    # The "+ 15" provides a small top margin inside the box
    screen.blit(text_canvas, (view_rect.x + 15, view_rect.y + 15 - scroll_y))
    screen.set_clip(None) 

    if gui_state.max_feedback_scroll > 0:
        bar_x = view_rect.right - 10
        bar_y = view_rect.y + 10
        bar_h = view_rect.height - 20
        
        # Track
        pygame.draw.rect(screen, (40, 40, 45), (bar_x, bar_y, 4, bar_h))
        
        # Thumb (the moving part)
        fraction = scroll_y / gui_state.max_feedback_scroll
        thumb_h = 30
        thumb_y = bar_y + (fraction * (bar_h - thumb_h))
        pygame.draw.rect(screen, header_color, (bar_x, thumb_y, 4, thumb_h), border_radius=2)

    # 4. Header Text
    pygame.draw.rect(screen, header_color, popup_rect, 4, border_radius=15)
    font = FONTS["transitionbutton"]
    msg_surf = font.render(msg, True, (255, 255, 255))
    msg_rect = msg_surf.get_rect(center=(popup_rect.centerx, popup_rect.y + 60))
    
    # Shadow
    shadow_surf = font.render(msg, True, (0, 0, 0))
    screen.blit(shadow_surf, msg_rect.move(3, 3))
    screen.blit(msg_surf, msg_rect)

    # 5. Button Logic
    current_popup_btn.rect.centerx = popup_rect.centerx
    current_popup_btn.rect.bottom = popup_rect.bottom - 25
    
    # Simple Hover Check
    mouse_pos = pygame.mouse.get_pos()
    # Note: If using scaling, use your virtual_mouse_pos here instead
    is_hover = current_popup_btn.rect.collidepoint(mouse_pos)
    btn_color = (30, 30, 35) if is_hover else (20, 20, 20)

    pygame.draw.rect(screen, btn_color, current_popup_btn.rect, border_radius=10)
    pygame.draw.rect(screen, COLORS["neon_purple"], current_popup_btn.rect, width=2, border_radius=10)

    # Button Label
    btn_text = current_popup_btn.textfont.render(current_popup_btn.text, True, COLORS["neon_purple"])
    screen.blit(btn_text, btn_text.get_rect(center=current_popup_btn.rect.center))

def draw_sidebar_panel(screen):
    sidebar_rect = pygame.Rect(0, 0, 200, 720)
    pygame.draw.rect(screen, COLORS["panel_dark"], sidebar_rect)
    pygame.draw.rect(screen, COLORS["panel_shadow"], (195, 0, 5, 720))
    pygame.draw.line(screen, COLORS["neon_purple"], (200, 0), (200, 720), 3)

def draw_guidebutton(screen, loader):
    # Stylized Guide button
    mouse = pygame.mouse.get_pos()
    is_hover = gs.GUIDE_RECT.collidepoint(mouse)

    # change color on hover
    bg_color = (30, 30, 35) if is_hover else (20, 20, 20)

    # background
    pygame.draw.rect(screen, bg_color, gs.GUIDE_RECT, border_radius=10)

    # border
    pygame.draw.rect(screen, COLORS["neon_purple"], gs.GUIDE_RECT, width=2, border_radius=10)

    guide_text = FONTS["guide"].render("GUIDE", True, COLORS["neon_purple"])
    guide_text_rect = guide_text.get_rect(center=gs.GUIDE_RECT.center)

    guide_shadow = FONTS["guide"].render("GUIDE", True, (100, 40, 150))
    guide_shadow_rect = guide_text_rect.move(2, 2)

    screen.blit(guide_shadow, guide_shadow_rect)
    screen.blit(guide_text, guide_text_rect)

    screen.blit(loader.health_icon, (562, 682))
    screen.blit(loader.shield_icon, (743, 682))

def draw_defenses(screen, defense_buttons, info_buttons, gui_state):
    current_y_offset = 140
    visible_count = 0
    first_y = 140
    button_height = 150
    max_cabinet_height = 500  # original cabinet height

    for i in range(len(defense_buttons)):
        btn = defense_buttons[i]
        info_btn = info_buttons[i]

        # Skip placed defenses so their cabinet space collapses
        if btn.was_placed:
            continue

        # Assign visible defense its cabinet position
        btn.base_y = current_y_offset
        info_btn.base_y = current_y_offset

        current_y_offset += button_height + gs.CASTLE_SPACING
        visible_count += 1

    # Total bottom of visible content
    if visible_count > 0:
        visible_content_height = (
            first_y
            + visible_count * button_height
            + (visible_count - 1) * gs.CASTLE_SPACING
        )
    else:
        visible_content_height = gs.CABINET_VIEW_RECT.y

    # How tall the cabinet should appear:
    # shrink when little content remains, but never exceed original height
    needed_height = max(0, visible_content_height - gs.CABINET_VIEW_RECT.y)
    gs.CABINET_VIEW_RECT.height = min(max_cabinet_height, needed_height)

    # Allow scrolling only if content is taller than the visible cabinet
    gui_state.max_scroll = max(0, needed_height - gs.CABINET_VIEW_RECT.height)
    gui_state.scroll_y = min(gui_state.scroll_y, gui_state.max_scroll)

    screen.set_clip(gs.CABINET_VIEW_RECT)

    screen.set_clip(gs.CABINET_VIEW_RECT)
    for i in range(len(defense_buttons)):
        btn = defense_buttons[i]
        info_btn = info_buttons[i]

        # CRITICAL: Only draw here if NOT placed AND NOT currently being dragged
        if not btn.was_placed and not btn.dragging:
            btn.update_scroll_position(gui_state.scroll_y)
            info_btn.update_scroll_position(gui_state.scroll_y)
            
            if btn.rect.colliderect(gs.CABINET_VIEW_RECT):
                btn.draw_button(screen)
                info_btn.draw_button(screen)

    screen.set_clip(None)
    # --- DRAW SCROLL BAR ---
    # Only draw if content is actually scrollable
    if gui_state.max_scroll > 0:
        bar_width = 8
        bar_margin = 5
        # The track is the height of your visible cabinet
        track_height = gs.CABINET_VIEW_RECT.height
        
        # Calculate how tall the handle (the moving part) should be
        # Handle height / Track height = Visible Area / Total Content Area
        total_content_height = needed_height
        handle_height = max(30, (track_height / total_content_height) * track_height)
        
        # Calculate vertical position
        # scroll_y / max_scroll gives us the percentage of scroll (0.0 to 1.0)
        scroll_pct = gui_state.scroll_y / gui_state.max_scroll
        scroll_pos_y = gs.CABINET_VIEW_RECT.y + (scroll_pct * (track_height - handle_height))
        
        # Define the bar rectangle (placed on the right edge of the cabinet)
        bar_rect = pygame.Rect(
            gs.CABINET_VIEW_RECT.right - bar_width - bar_margin,
            scroll_pos_y,
            bar_width,
            handle_height
        )
        
        # Draw the background track (optional, for better UI)
        track_rect = pygame.Rect(
            gs.CABINET_VIEW_RECT.right - bar_width - bar_margin,
            gs.CABINET_VIEW_RECT.y,
            bar_width,
            track_height
        )
        pygame.draw.rect(screen, (40, 40, 40), track_rect, border_radius=4)
        
        # Draw the actual handle
        pygame.draw.rect(screen, COLORS["neon_purple"], bar_rect, border_radius=4)

def draw_lock_button(buttons, state, screen):
    mouse = pygame.mouse.get_pos()
    is_hover = buttons["lock"].rect.collidepoint(mouse)

    # state check
    is_locked = state != "BUILD_PHASE"

    if is_locked:
        bg_color = (20, 20, 20)
    else:
        bg_color = (30, 30, 35) if is_hover else (20, 20, 20)

    # text + colors
    if not is_locked:
        button_text = "LAUNCH ATTACK"
        button_color = COLORS["neon_purple"]
        shadow_color = (100, 40, 150)   # purple shadow
    else:
        button_text = "ATTACK LAUNCHED"
        button_color = COLORS["danger_red"]
        shadow_color = (120, 20, 20)    

    # draw background
    pygame.draw.rect(screen, bg_color, buttons["lock"].rect, border_radius=10)

    # draw border
    pygame.draw.rect(screen, button_color, buttons["lock"].rect, width=2, border_radius=10)

    # font
    lock_font = buttons["lock"].textfont

    text = lock_font.render(button_text, True, button_color)
    text_rect = text.get_rect(center=buttons["lock"].rect.center)

    shadow = lock_font.render(button_text, True, shadow_color)
    shadow_rect = text_rect.move(2, 2)

    screen.blit(shadow, shadow_rect)
    screen.blit(text, text_rect)

import pygame

def draw_trash_can(screen, loader, rect, is_hovered=False):
    # --- PHASE 1: Recalculate Proportional Drawing ---
    img_rect = loader.trash_can_img.get_rect()
    aspect_ratio = img_rect.width / img_rect.height

    # Define base height (80% of collision box)
    base_h = int(rect.height * 0.8)
    # Calculate proportional width
    base_w = int(base_h * aspect_ratio)

    # --- PHASE 2: Scale the Sprite ---
    if is_hovered:

        # 1. Bump the overall size slightly (110%)
        final_w = int(base_w * 1.1)
        final_h = int(base_h * 1.1)
        
        # 2. Scale the original sprite
        temp_img = pygame.transform.smoothscale(loader.trash_can_img, (final_w, final_h))
        
        # 3. Create the LIGHT Red Tint Overlay
        tint_surface = pygame.Surface((final_w, final_h)).convert_alpha()
        
        # CHANGE THIS: (255, 200, 200) creates a much softer, lighter tint.
        # The closer these numbers are to 255, the lighter the tint will be.
        tint_surface.fill((255, 100, 100)) 
        
        # 4. Merge
        tint_surface.blit(temp_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        final_img = tint_surface
    else:
        # Standard size (80% of rect)
        final_w = base_w
        final_h = base_h
        final_img = pygame.transform.smoothscale(loader.trash_can_img, (final_w, final_h))

    # --- PHASE 3: Draw Centered ---
    # Center the scaled image within the larger collision rectangle
    pos_x = rect.centerx - (final_w // 2)
    pos_y = rect.centery - (final_h // 2)

    screen.blit(final_img, (pos_x, pos_y))