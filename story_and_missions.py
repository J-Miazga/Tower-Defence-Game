import pygame as pg

class StoryManager:
    def __init__(self, screen, font): 
        # Initializes popup system with screen reference and font
        self.screen = screen
        self.font = font
        self.screen_width, self.screen_height = screen.get_size()
        self.popup_width = self.screen_width - 40
        self.popup_height = self.screen_height - 100

    def show_popup(self, message):
        """
        Displays a centered popup with text and an OK button. 
        Freezes game until player clicks to continue.
        """
        # Calculate center position for popup box
        popup_x = (self.screen_width - self.popup_width) // 2
        popup_y = (self.screen_height - self.popup_height) // 2
        popup_rect = pg.Rect((popup_x, popup_y, self.popup_width, self.popup_height))
        
        # Position OK button at bottom of popup
        button_width = 100
        button_height = 40
        button_x = popup_x + (self.popup_width - button_width) // 2
        button_y = popup_y + self.popup_height - button_height - 20
        button_rect = pg.Rect((button_x, button_y, button_width, button_height))
        
        # Break message into lines that fit the popup width
        wrapped_lines = self.wrap_text(message, self.font, self.popup_width - 40)
        
        # Dark transparent overlay behind popup
        overlay = pg.Surface((self.screen_width, self.screen_height), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        running = False  # Exit popup
            
            # Draw popup background
            pg.draw.rect(self.screen, (220, 220, 220), popup_rect, border_radius=10)
            pg.draw.rect(self.screen, (50, 150, 50), button_rect, border_radius=8)
            
            # Draw each line of wrapped text, centered vertically
            line_height = self.font.get_linesize()
            total_text_height = line_height * len(wrapped_lines)
            start_y = popup_rect.centery - total_text_height // 2
            
            for i, line in enumerate(wrapped_lines):
                text_surface = self.font.render(line, True, (0, 0, 0))
                text_rect = text_surface.get_rect(centerx=popup_rect.centerx, 
                                                  top=start_y + i * line_height)
                self.screen.blit(text_surface, text_rect)
            
            # Draw OK button text
            btn_text = self.font.render("OK", True, (255, 255, 255))
            btn_rect = btn_text.get_rect(center=button_rect.center)
            self.screen.blit(btn_text, btn_rect)
            
            pg.display.flip()

    def wrap_text(self, text, font, max_width):
        """
        Splits a long string into multiple lines based on max_width.
        """
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_width, _ = font.size(test_line)
            
            if test_width <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines

class MissionManager:
    def __init__(self):
        # Initializes mission-related flags and text
        self.current_mission = ""
        self.mission_active = False
        self.reward_given = False

    def set_mission(self, mission_text):
        """
        Start a new mission by setting its description and enabling it.
        """
        self.current_mission = mission_text
        self.mission_active = True
        self.reward_given = False

    def check_upgrade_mission(self, turret_group, game_map):
        """
        Check if the upgrade mission condition is met (any turret upgraded).
        If so, give the reward and complete the mission.
        """
        if self.mission_active and not self.reward_given:
            for turret in turret_group:
                if turret.upgrade_turret > 1:
                    game_map.money += 300 
                    self.reward_given = True
                    self.mission_active = False
                    self.current_mission = ""
                    return True
        return False

    def draw_mission(self, screen, font):
        """
        Render the mission text in a transparent box on the screen.
        """
        if not self.mission_active or not self.current_mission:
            return

        mission_surface = pg.Surface((300, 50), pg.SRCALPHA)
        mission_surface.fill((100, 100, 100, 100))  # semi-transparent background

        mission_text = f"Mission: {self.current_mission}"
        text_render = font.render(mission_text, True, (255, 255, 255))
        text_rect = text_render.get_rect(topleft=(10, 10))

        screen.blit(mission_surface, (0, 0))
        screen.blit(text_render, text_rect)
