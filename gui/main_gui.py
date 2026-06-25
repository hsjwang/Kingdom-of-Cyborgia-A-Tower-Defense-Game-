import pygame, sys, random, math
from pathlib import Path
from engine.game_server import GameServer
from engine.schema import attacks_dict
import gui.design_specs as gs
import gui.view_renderer as gd
from gui.design_specs import FONTS, COLORS
from gui.button import createDefenseButtons, init_game_buttons
from gui.gui_state import UIState
from gui.image_handling import Loader

def main():
    try:

        if getattr(sys, "frozen", False):
            BASE_DIR = Path(sys.executable).resolve().parent
        else:
            BASE_DIR = Path(__file__).resolve().parent.parent

        # Setup 
        pygame.init()
        pygame.font.init()
        actual_screen = pygame.display.set_mode((gs.SCREEN_RES), pygame.RESIZABLE)
        screen = pygame.Surface(gs.SCREEN_RES)
        clock = pygame.time.Clock()

        # Helpers 
        server = GameServer()
        loader = Loader()
        gui_state = UIState()
        buttons = init_game_buttons(server)

        # Dynamic Lists 
        active_attack_sprites = []
        fire_list = []
        particles = []
        defense_buttons = []
        info_buttons = []

        buttons = init_game_buttons(server)

        # Initial Setup for dynamic buttons 
        createDefenseButtons(defense_buttons, server, gs.CASTLE_SPACING, info_buttons, loader.defense_images)

        content_height = 140 + len(defense_buttons) * (150 + gs.CASTLE_SPACING)
        gui_state.max_scroll = max(0, content_height - gs.CABINET_VIEW_RECT.height)

        running = True
        while running:
            win_w, win_h = actual_screen.get_size()
            scale_x = gs.SCREEN_RES[0] / win_w
            scale_y = gs.SCREEN_RES[1] / win_h

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if hasattr(event, 'pos'):
                    # Translate window coordinates to virtual coordinates
                    virtual_mouse_pos = (event.pos[0] * scale_x, event.pos[1] * scale_y)
                    # Overwrite the event position so all your .collidepoint calls work
                    event.pos = virtual_mouse_pos
                # ---------------- ATTACK POPUP SCREEN EVENTS ----------------
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and gui_state.showing_narrative:
                    if gs.NARRATIVE_CONTINUE_RECT.collidepoint(event.pos):
                        if gui_state.narrative_index < len(server.current_level_attacks) - 1:
                            gui_state.narrative_index += 1
                        else:
                            gui_state.showing_narrative = False # Close popup and start build period
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if (server.level >=3 or server.player_health <= 0) and gui_state.showing_feedback:
                            defense_buttons, info_buttons = gui_state.reset_game(server, defense_buttons, fire_list, particles, loader, gs.CASTLE_SPACING, info_buttons)
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        defense_buttons, info_buttons = gui_state.reset_game(server, defense_buttons, fire_list, particles, loader, gs.CASTLE_SPACING, info_buttons)
                if event.type == pygame.MOUSEWHEEL:
                    if (server.level >=3 or server.player_health <= 0) and gui_state.showing_feedback:
                        # Increase scroll_y
                        gui_state.feedback_scroll_y -= event.y * 30 
                        
                        # Clamp to bounds
                        max_s = getattr(gui_state, 'max_feedback_scroll', 0)
                        if gui_state.feedback_scroll_y < 0:
                            gui_state.feedback_scroll_y = 0
                        if gui_state.feedback_scroll_y > max_s:
                            gui_state.feedback_scroll_y = max_s
                    if server.state in ["NEXT_LEVEL", "LEVEL_FAILED"]:
                        gui_state.feedback_scroll_y -= event.y * 25 # Increased speed slightly
                        
                        # Clamp between 0 and the max scroll height
                        max_scroll = getattr(gui_state, 'max_feedback_scroll', 0)
                        gui_state.feedback_scroll_y = max(0, min(gui_state.feedback_scroll_y, max_scroll))

                # ---------------- TITLE SCREEN EVENTS ----------------
                if gui_state.game_state == "Title Screen":
                    # If the guidebook is open, do NOT let Play/Guide title buttons receive clicks underneath it
                    if not gui_state.show_guidebook:
                        cmd = buttons["play"].check_click(event, gui_state.scroll_y, gs.FIELD_RECT)
                        if cmd == "START_GAME":
                            print(server.parse_command("START_GAME"))
                            start_ticks = pygame.time.get_ticks()
                            gui_state.game_state = "Game Screen"
                
                        guide_cmd = buttons["title_guide"].check_click(event, gui_state.scroll_y, gs.FIELD_RECT)
                        if guide_cmd == "OPEN_GUIDE":
                            gui_state.show_guidebook = True
                            gui_state.guidebook_section = "menu"
                            gui_state.guidebook_page = 0

                # ---------------- GUIDEBOOK EVENTS (WORKS ON TITLE + GAME SCREEN) ----------------
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and gui_state.show_guidebook:
                    if gs.CLOSE_RECT.collidepoint(event.pos):
                        gui_state.show_guidebook = False

                    elif gui_state.guidebook_section != "menu" and gs.BACK_RECT.collidepoint(event.pos):
                        gui_state.guidebook_section = "menu"
                        gui_state.guidebook_page = 0

                    elif gui_state.guidebook_section == "menu":
                        if gs.MENU_HOWTO_RECT.collidepoint(event.pos):
                            gui_state.guidebook_section = "how_to_play"
                            gui_state.guidebook_page = 0

                        elif gs.MENU_DEFENSES_RECT.collidepoint(event.pos):
                            gui_state.guidebook_section = "defenses"
                            gui_state.guidebook_page = 0

                    else:
                        if gs.LEFT_PAGE_TURN_RECT.collidepoint(event.pos) and gui_state.guidebook_page > 0:
                            gui_state.guidebook_page -= 1

                        elif gs.RIGHT_PAGE_TURN_RECT.collidepoint(event.pos):
                            if gui_state.guidebook_section == "how_to_play":
                                current_pages = gs.HOW_TO_PLAY_DATA
                            else:
                                current_pages = gs.DEFENSE_GUI_PAGES

                            if gui_state.guidebook_page < len(current_pages) - 1:
                                gui_state.guidebook_page += 1

                # ---------------- GAME SCREEN EVENTS ----------------
                if gui_state.game_state == "Game Screen":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # GUARD: Cannot open Intel Reports if Guidebook or Narrative is already visible
                        if not gui_state.show_guidebook and not gui_state.showing_narrative: 
                            if buttons["report"].rect.collidepoint(event.pos) and server.state == "BUILD_PHASE":
                                gui_state.showing_narrative = True
                                gui_state.narrative_index = 0
                                gui_state.narrative_opened_for_level = True # Flag as opened so it stops pulsing
                        
                        # Check RESET button separately (Keep this outside the intel guard)
                        if buttons["reset"].rect.collidepoint(event.pos):
                            defense_buttons, info_buttons = gui_state.reset_game(server, defense_buttons, fire_list, particles, loader, gs.CASTLE_SPACING, info_buttons)

                    # GUARD: Block sidebar info interaction if any popup/modal is active
                    if not gui_state.showing_narrative and not gui_state.show_guidebook:
                        for i, info_btn in enumerate(info_buttons): # Add enumerate here
                            # Only allow interaction if the defense hasn't been placed 
                            if not defense_buttons[i].was_placed:
                                cmd = info_btn.check_click(event, gui_state.scroll_y, gs.FIELD_RECT, allow_drag=False)
                                
                                if cmd and cmd.startswith("INFO_"):
                                    page_idx = int(cmd.split("_")[1])
                                    gui_state.show_guidebook = True
                                    gui_state.guidebook_section = "defenses"
                                    gui_state.guidebook_page = page_idx
                            
                    # Trigger narrative if we just entered a new level's Build Phase
                    if server.state == "BUILD_PHASE" and server.level > gui_state.last_seen_level:
                        gui_state.narrative_index = 0
                        gui_state.last_seen_level = server.level
                        gui_state.narrative_opened_for_level = False # Reset flag for the new level
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if buttons["reset"].rect.collidepoint(event.pos):
                            defense_buttons, info_buttons = gui_state.reset_game(server, defense_buttons, fire_list, particles, loader, gs.CASTLE_SPACING, info_buttons)

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        # Open in-game guidebook
                        if gs.GUIDE_RECT.collidepoint(event.pos):
                            gui_state.show_guidebook = True
                            guidebook_section = "menu"
                            guidebook_page = 0

                    allow_drag = (server.state == "BUILD_PHASE") and (not gui_state.show_guidebook) and (not gui_state.showing_narrative)

                    if event.type == pygame.MOUSEWHEEL:
                        if gs.CABINET_VIEW_RECT.collidepoint(pygame.mouse.get_pos()):
                            gui_state.scroll_y -= event.y * gs.SCOLL_SPEED
                            gui_state.scroll_y = max(0, min(gui_state.scroll_y, gui_state.max_scroll))

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if gs.CABINET_VIEW_RECT.collidepoint(pygame.mouse.get_pos()):
                            if event.button == 4:
                                gui_state.scroll_y = max(0, gui_state.scroll_y - gs.SCOLL_SPEED)
                            elif event.button == 5:
                                gui_state.scroll_y = min(gui_state.max_scroll, gui_state.scroll_y + gs.SCOLL_SPEED)

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if buttons["lock"].rect.collidepoint(event.pos) and server.state == "BUILD_PHASE":
                            # 1. Lock and Launch
                            print(server.parse_command("LOCK_DEFENSES"))
                            server.parse_command("LAUNCH_ATTACK")
                            
                            # 2. Initialize Animation Sprites
                            active_attack_sprites.clear()
                            attack_auto_timer = pygame.time.get_ticks()
                            
                            for i, attack_id in enumerate(server.current_level_attacks):
                                # Start attacks from off-screen right at random heights
                                start_x = 1300
                                start_y = 150 + (i * 120) 
                                # Target the middle of the castle sockets area
                                target = (850, 360) 
                                
                                active_attack_sprites.append({
                                    "id": attack_id,
                                    "pos": [start_x, start_y],
                                    "target": target,
                                    "speed": random.uniform(3.0, 5.0)
                                })

                    for btn in defense_buttons:
                        btn.check_click(event, gui_state.scroll_y, gs.FIELD_RECT, allow_drag=allow_drag)
                    
                    if server.state == "NEXT_LEVEL":
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if buttons["next_level"].rect.collidepoint(event.pos):
                                print(server.parse_command(buttons["next_level"].command))
                                createDefenseButtons(defense_buttons, server, gs.CASTLE_SPACING, info_buttons, loader.defense_images) # Reset the Defenses 
                                gui_state.feedback_generated = False # Reset for the next victory
                                gui_state.showing_feedback = False
                                gui_state.feedback_scroll_y = 0
                        continue  # Block background clicks

                    elif server.state == "LEVEL_FAILED":
                        
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if buttons["retry_level"].rect.collidepoint(event.pos):
                                print(server.parse_command(buttons["retry_level"].command))
                                gui_state.feedback_generated = False # Reset for the next potential failure
                                gui_state.showing_feedback = False
                                gui_state.feedback_scroll_y = 0
                        continue  # Block background clicks

            # ---------------- DRAW TITLE SCREEN ----------------
            if gui_state.game_state == "Title Screen":
                gd.draw_title_screen(screen, server.player_health, gui_state, loader, buttons["play"], buttons["title_guide"])

            # ---------------- DRAW GAME SCREEN ----------------
            elif gui_state.game_state == "Game Screen":

                # Draw the current Background 
                if server.level >= 3 and server.state == "NEXT_LEVEL": 
                    loader.current_bg = loader.get_current_bg(server.player_health - 25)
                else: 
                    loader.current_bg = loader.get_current_bg(server.player_health)
                screen.blit(loader.current_bg, (100, 0))

                # If player has lost game and the animation hasn't been played yet, then show the loss animation  
                if server.player_health <= 0 and not gui_state.showing_feedback:
                    gd.draw_loss_animation(screen, gui_state, fire_list, loader.current_bg, loader)

                gd.draw_sidebar_panel(screen)
                gd.draw_budget(screen, server.player_budget)
                gd.draw_game_titles(screen, server.level, server.state)
                gd.draw_reset_button(screen, buttons["reset"])
                gd.draw_guidebutton(screen, loader)
                gd.draw_intel_report(screen, server.state, server.current_level_attacks, buttons["report"], gui_state)
                gd.draw_lock_button(buttons, server.state, screen)

                # Draw health and shield bars 
                if server.player_health > 100: 
                    gd.draw_health_bar(screen, 586.5, 683, 150, 18, 100, max_health=100)
                    gd.draw_shield_bar(screen, 767, 683, 150, 18, server.player_health - 100, max_health=100)
                else :
                    gd.draw_health_bar(screen, 586, 683, 150, 18, server.player_health, max_health=100)
                    gd.draw_shield_bar(screen, 767, 683, 150, 18, 0, max_health=100)

                hovering_trash = False
                for btn in defense_buttons:
                    if btn.dragging and btn.rect.colliderect(gs.TRASH_CAN_RECT):
                        hovering_trash = True
                        break

                # Draw the trash can
                gd.draw_trash_can(screen, loader, gs.TRASH_CAN_RECT, hovering_trash)
        
                
                # Draw Defenses
                gd.draw_defenses(screen, defense_buttons, info_buttons, gui_state)
                if server.player_health > 0 :
                    # Draw placed/dragged defenses outside clip
                    for btn in defense_buttons:
                        if btn.was_placed or btn.dragging:
                            btn.draw_button(screen)

                # Draw and animate the attack sprites if the attack is happening 
                if server.state == "ATTACK_PHASE":
                    for sprite in active_attack_sprites:
                        gd.draw_attack_sprite(screen, loader, sprite)

                    if pygame.time.get_ticks() - attack_auto_timer > gs.ATTACK_DURATION:
                        # This triggers the server to change state to NEXT_LEVEL or LEVEL_FAILED
                        result = server.resolve_round() 
                        active_attack_sprites.clear()
                        feedback_generated = False
                
                # If player has won game and the animation hasn't been played yet, then show the win animation  
                if server.level >= 3 and server.state == "NEXT_LEVEL" and not gui_state.showing_feedback:
                    gd.draw_win_animation(screen, gui_state, loader, particles)

                if (server.state in ["NEXT_LEVEL", "LEVEL_FAILED", "GAME_OVER"]) and not gui_state.feedback_generated:
                    server.parse_command("GET_FEEDBACK")
                    gui_state.feedback_generated = True

                if gui_state.show_guidebook:
                    gd.draw_guidebook(screen, gui_state, loader)

                if gui_state.showing_narrative:
                    gd.draw_narrative_popup(screen, gui_state, server.current_level_attacks, loader)

                if server.player_health <= 0 and gui_state.showing_feedback:
                    gd.draw_game_over(screen, server.level, server.player_budget, gui_state, server.feedback_body) 
                if server.state == "NEXT_LEVEL" and server.level >=3 and gui_state.showing_feedback:
                    gd.draw_victory_screen(screen, server.feedback_body, gui_state)

                if (server.state == "LEVEL_FAILED" and server.player_health > 0) or (server.state == "NEXT_LEVEL" and server.level < 3):
                    gui_state.showing_feedback = True
                    gd.draw_feedback(screen, server.state, buttons, server.feedback_title, server.feedback_body, gui_state)

            # Scale to screen size (display screen is adjustable by user)
            scaled_win = pygame.transform.scale(screen, actual_screen.get_size())
            
            # Blit the scaled image onto the actual window monitor
            actual_screen.blit(scaled_win, (0, 0))
            
            # Update the physical display
            pygame.display.flip() 
            clock.tick(60)

    except KeyboardInterrupt:
        print("\n[System] Keyboard Interrupt detected. Closing game safely...")
    finally:
        # This code runs no matter what (crash or interrupt)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
