import pygame 
from gui.design_specs import FONTS, CASTLE_SOCKETS, NARRATIVE_NAMES, VISIBLE_DEFENSES, COLORS, TRASH_CAN_RECT
from engine.schema import defenses_dict

class Button:
    def __init__(self, xpos, ypos, width, height, text,
                 textcolor, textfont,
                 buttoncolor, hovercolor,
                 bordercolor, borderpt, command=None, draggable=False,
                 defense_key=None, image=None, server=None):

        self.rect = pygame.Rect(xpos, ypos, width, height)
        self.text = text
        self.textcolor = textcolor
        self.textfont = textfont
        self.buttoncolor = buttoncolor
        self.hovercolor = hovercolor
        self.bordercolor = bordercolor
        self.borderpt = borderpt
        self.command = command

        self.draggable = draggable
        self.dragging = False
        self.was_placed = False

        self.offset_x = 0
        self.offset_y = 0

        self.start_x = xpos
        self.start_y = ypos
        self.base_x = xpos
        self.base_y = ypos

        self.defense_key = defense_key
        self.image = image
        self.image_offset_y = -13   # image sits a little above center
        self.server = server 

    def get_image_rect(self):
        if self.image is None:
            return None
        return self.image.get_rect(center=(self.rect.centerx, self.rect.centery + self.image_offset_y))

    def reset_to_cabinet(self, scroll_y):
        self.rect.x = self.base_x
        self.rect.y = self.base_y - scroll_y

    def update_scroll_position(self, scroll_y):
        if self.draggable and not self.was_placed and not self.dragging:
            self.reset_to_cabinet(scroll_y)

    def draw_button(self, screen):
        win_w, win_h = pygame.display.get_surface().get_size()
        raw_m = pygame.mouse.get_pos()
        mousepos = (raw_m[0] * (1280/win_w), raw_m[1] * (720/win_h))
        image_rect = self.get_image_rect()
        hover_rect = image_rect if (image_rect is not None and not self.was_placed) else self.rect

        bg_color = (30, 30, 35) if hover_rect.collidepoint(mousepos) else (15, 15, 18)
        neon_purple = (180, 80, 255)
        text_white = (255, 255, 255)

        if not self.was_placed:
            pygame.draw.rect(screen, bg_color, self.rect, border_radius=self.borderpt)
            pygame.draw.rect(screen, neon_purple, self.rect, width=2, border_radius=self.borderpt)

        if self.image is not None and image_rect is not None:
            screen.blit(self.image, image_rect)

            if self.defense_key is not None and not self.was_placed:
                # Pull from NARRATIVE_NAMES in gui_schema
                display_name = NARRATIVE_NAMES.get(self.defense_key, self.defense_key) #
                
                name_surface = FONTS["dfont"].render(display_name, True, text_white) #
                cost_surface = FONTS["dfont"].render(f"${defenses_dict[self.defense_key].cost}", True, (180, 80, 255))

                name_rect = name_surface.get_rect(center=(self.rect.centerx, self.rect.bottom - 30))
                cost_rect = cost_surface.get_rect(center=(self.rect.centerx, self.rect.bottom - 13))
                screen.blit(name_surface, name_rect)
                screen.blit(cost_surface, cost_rect)

        else:
            button_surface = self.textfont.render(self.text, True, neon_purple)
            button_text = button_surface.get_rect(center=self.rect.center)
            screen.blit(button_surface, button_text)
        
        target = CASTLE_SOCKETS.get(self.defense_key)
        if target and self.dragging:
            x, y = target
            size = 35      # The overall spread of the brackets
            line_len = 12  # How long the corner lines are
            x_size = 10    # The size of the 'X' in the middle
            color = (255, 50, 50) # red
            line_thickness = 4

            # --- 1. Draw the Corner Brackets ---
            # Top Left
            pygame.draw.lines(screen, color, False, [(x-size, y-size+line_len), (x-size, y-size), (x-size+line_len, y-size)], line_thickness)
            # Top Right
            pygame.draw.lines(screen, color, False, [(x+size-line_len, y-size), (x+size, y-size), (x+size, y-size+line_len)], line_thickness)
            # Bottom Left
            pygame.draw.lines(screen, color, False, [(x-size, y+size-line_len), (x-size, y+size), (x-size+line_len, y+size)], line_thickness)
            # Bottom Right
            pygame.draw.lines(screen, color, False, [(x+size-line_len, y+size), (x+size, y+size), (x+size, y+size-line_len)], line_thickness)

            # --- 2. Draw the 'X' in the Middle ---
            # Backslash part of X (\)
            pygame.draw.line(screen, color, (x - x_size, y - x_size), (x + x_size, y + x_size), line_thickness)
            # Slash part of X (/)
            pygame.draw.line(screen, color, (x + x_size, y - x_size), (x - x_size, y + x_size), line_thickness) 
    
    def snap_to_grid(self, x, y):
        grid_size = 80
        snapped_x = round(x / grid_size) * grid_size
        snapped_y = round(y / grid_size) * grid_size
        return snapped_x, snapped_y
    
    def snap_center_to_grid(self, center_x, center_y, width, height):
        snapped_center_x, snapped_center_y = self.snap_to_grid(center_x, center_y)
        snapped_x = snapped_center_x - width // 2
        snapped_y = snapped_center_y - height // 2
        return snapped_x, snapped_y

    def check_click(self, event, scroll_y, field_rect, allow_drag=True):
        if self.draggable:
            self.update_scroll_position(scroll_y)

        image_rect = self.get_image_rect()
        hit_rect = image_rect if image_rect is not None else self.rect

        if event.type == pygame.MOUSEBUTTONDOWN:
            if hit_rect.collidepoint(event.pos):
                if self.draggable and allow_drag:
                    self.dragging = True
                    mouse_x, mouse_y = event.pos
                    self.offset_x = self.rect.x - mouse_x
                    self.offset_y = self.rect.y - mouse_y
                return self.command

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.dragging = False
                
                # --- FEATURE: Remove Defense by Dragging to Trash Can ---
                if self.rect.colliderect(TRASH_CAN_RECT): 
                    if self.was_placed:
                        response = self.server.parse_command(f"REMOVE_DEFENSE {self.defense_key}")
                        print(response)
                        if "removed" in response.lower():
                            self.was_placed = False
                            self.reset_to_cabinet(scroll_y)
                        else:
                            # Server said no, snap back to socket
                            target_pos = CASTLE_SOCKETS.get(self.defense_key)
                            if target_pos:
                                self.rect.center = target_pos
                    else:
                        # Dragged from cabinet but dropped in trash; just return home
                        self.reset_to_cabinet(scroll_y)
                    return None

                # --- PLACEMENT / SNAP LOGIC ---
                target_pos = CASTLE_SOCKETS.get(self.defense_key)
                
                if target_pos:
                    mouse_pos = event.pos
                    dist = pygame.math.Vector2(mouse_pos).distance_to(target_pos)

                    if dist < 70: 
                        if not self.was_placed:
                            response = self.server.parse_command(f"BUILD_DEFENSE {self.defense_key}")
                            print(response)

                            if "built successfully" in response.lower():
                                self.rect.center = target_pos
                                self.was_placed = True
                            else:
                                self.reset_to_cabinet(scroll_y)
                        else:
                            # Already placed, just snap it perfectly back into place
                            self.rect.center = target_pos
                    else:
                        if self.was_placed:
                            self.rect.center = target_pos # Snap back if they drop it randomly on field
                        else:
                            self.reset_to_cabinet(scroll_y)
                else:
                    # FALLBACK FIELD LOGIC (For defenses without strict sockets)
                    center_in_field = field_rect.collidepoint(self.rect.center)
                    
                    if allow_drag and center_in_field:
                        if not self.was_placed:
                            response = self.server.parse_command(f"BUILD_DEFENSE {self.defense_key}")
                            print(response)
                            
                            if "built successfully" in response.lower():
                                snapped_x, snapped_y = self.snap_center_to_grid(
                                    self.rect.centerx, self.rect.centery,
                                    self.rect.width, self.rect.height
                                )
                                self.rect.x = max(field_rect.left, min(snapped_x, field_rect.right - self.rect.width))
                                self.rect.y = max(field_rect.top, min(snapped_y, field_rect.bottom - self.rect.height))
                                self.was_placed = True
                            else:
                                self.reset_to_cabinet(scroll_y)
                        else:
                            # Move existing placement around the field
                            snapped_x, snapped_y = self.snap_center_to_grid(
                                self.rect.centerx, self.rect.centery,
                                self.rect.width, self.rect.height
                            )
                            self.rect.x = max(field_rect.left, min(snapped_x, field_rect.right - self.rect.width))
                            self.rect.y = max(field_rect.top, min(snapped_y, field_rect.bottom - self.rect.height))
                    else:
                        self.reset_to_cabinet(scroll_y)

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging and allow_drag:
                mouse_x, mouse_y = event.pos
                self.rect.x = mouse_x + self.offset_x
                self.rect.y = mouse_y + self.offset_y

        return None

def createDefenseButtons(defense_buttons, server, castle_spacing, info_buttons, defense_images):
    if defense_buttons: 
        defense_buttons.clear()
        info_buttons.clear()
        
    for i, defense_key in enumerate(VISIBLE_DEFENSES):
        y = 140 + i * (150 + castle_spacing)
        
        # Main Defense Button
        new_btn = Button(
            23, y, 150, 150, "",
            COLORS["black"], FONTS["playbutton"],
            COLORS["cabinet_icons"], COLORS["cabinet_icons_hover"], COLORS["black"], 15,
            draggable=True,
            defense_key=defense_key,
            image=defense_images[defense_key],
            server=server
        )

        # --- NEW PERSISTENCE LOGIC ---
        # If the server already knows this defense is active (from a previous level),
        # visually place it on the board immediately.
        if defense_key in server.active_defenses:
            new_btn.was_placed = True
            target_pos = CASTLE_SOCKETS.get(defense_key)
            if target_pos:
                new_btn.rect.center = target_pos

        defense_buttons.append(new_btn)
        
        # New (+) Info Button
        # Index 'i' matches the index in DEFENSE_GUI_PAGES
        info_buttons.append(
            Button(
                143, y, 30, 30, "?",
                (255, 255, 255), FONTS["guide_text"],
                (60, 20, 80), (100, 40, 150), 
                (180, 80, 255), 5,
                command=f"INFO_{i}",
                draggable=True, 
                server=server
            )
        )

### Init Game Buttons Function ###
def init_game_buttons(server):
    return {
        "play": Button(
                    490, 400, 300, 100,
                    text="PLAY",
                    textcolor=COLORS["black"],
                    textfont=FONTS["playbutton"],
                    buttoncolor=COLORS["yellow_startbutton"],
                    hovercolor=(199, 198, 197),
                    bordercolor=COLORS["black"],
                    borderpt=15,
                    command="START_GAME",
                    server=server
                ),
        "report": Button(
                    1025, 50, 230, 60, 
                    text="INTEL REPORT",
                    textcolor=COLORS["danger_red"],
                    textfont=FONTS["btn_font_24"],
                    buttoncolor=(20, 20, 20), 
                    hovercolor=(40, 20, 20),
                    bordercolor=COLORS["danger_red"],
                    borderpt=10,
                    command="OPEN_NARRATIVE",
                    server=server
                ),
        "title_guide": Button(
                        490, 515, 300, 100,
                        text="GUIDE",
                        textcolor=COLORS["black"],
                        textfont=FONTS["playbutton"],
                        buttoncolor=COLORS["yellow_startbutton"],
                        hovercolor=(199, 198, 197),
                        bordercolor=COLORS["black"],
                        borderpt=15,
                        command="OPEN_GUIDE",
                        server=server
                    ),
        "lock": Button(
                    25, 650, 150, 50, 
                    text="LAUNCH ATTACK",
                    textcolor=(255, 255, 255),
                    textfont=FONTS["lock_font"],
                    buttoncolor=(15, 15, 18), 
                    hovercolor=(199, 198, 197),
                    bordercolor=(180, 80, 255),
                    borderpt=10,
                    command="LOCK_DEFENSES",
                    server=server
                ),
        "next_level": Button(
                        540, 370, 200, 50, 
                        text="NEXT LEVEL",
                        textcolor=(255, 255, 255),
                        textfont=FONTS["btn_font_21"],
                        buttoncolor=(15, 15, 18), 
                        hovercolor=(30, 30, 35),
                        bordercolor=(80, 255, 150),  # Green
                        borderpt=5,
                        command="NEXT_LEVEL",
                        server=server
                    ),
        "retry_level": Button(
                            540, 370, 200, 50, 
                            text="RETRY LEVEL",
                            textcolor=(255, 255, 255),
                            textfont=FONTS["btn_font_21"],
                            buttoncolor=(15, 15, 18), 
                            hovercolor=(30, 30, 35),
                            bordercolor=(255, 80, 80),  # Red
                            borderpt=5,
                            command="RETRY_LEVEL",
                            server=server
                        ),
        "reset": Button(
                    1100, 630, 150, 50, 
                    text="RESET GAME",
                    textcolor=(255, 255, 255),
                    textfont=FONTS["btn_font_21"],
                    buttoncolor=(40, 10, 10),    
                    hovercolor=(199, 198, 197),    
                    bordercolor=(255, 50, 50),   
                    borderpt=5,
                    command="RESET",              
                    server=server
                )
    }
