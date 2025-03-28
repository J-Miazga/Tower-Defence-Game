# import pygame as pg

# class GameUIManager:
#     def __init__(self, screen, font): 
#         self.screen = screen
#         self.font = font
#         self.screen_width, self.screen_height = screen.get_size()
#         self.current_mission = ""
#         self.mission_completed = False
#         self.turret_upgraded_first_time = False
#         self.gold_reward_given = False
#         self.popup_width =  self.screen_width -40
#         self.popup_height =  self.screen_height -100

#     def show_popup(self, message):
#         # Centered popup positioning
#         popup_x = (self.screen_width - self.popup_width) // 2
#         popup_y = (self.screen_height - self.popup_height) // 2
#         popup_rect = pg.Rect((popup_x, popup_y, self.popup_width, self.popup_height))
        
#         # Button positioning relative to popup
#         button_width = 100
#         button_height = 40
#         button_x = popup_x + (self.popup_width - button_width) // 2
#         button_y = popup_y + self.popup_height - button_height - 20
#         button_rect = pg.Rect((button_x, button_y, button_width, button_height))
        

#         # Wrap the text
#         wrapped_lines = self.wrap_text(message, self.font, self.popup_width - 40)
        
#         # Dark overlay
#         overlay = pg.Surface((self.screen_width, self.screen_height), pg.SRCALPHA)
#         overlay.fill((0, 0, 0, 128))  # Semi-transparent black
#         self.screen.blit(overlay, (0, 0))
        
#         running = True
#         while running:
#             for event in pg.event.get():
#                 if event.type == pg.QUIT:
#                     pg.quit()
#                     exit()
#                 if event.type == pg.MOUSEBUTTONDOWN:
#                     if button_rect.collidepoint(event.pos):
#                         running = False  # Close popup
            
#             # Popup rectangle
#             pg.draw.rect(self.screen, (220, 220, 220), popup_rect, border_radius=10)
#             pg.draw.rect(self.screen, (50, 150, 50), button_rect, border_radius=8)
            
#             # Render wrapped text
#             line_height = self.font.get_linesize()
#             total_text_height = line_height * len(wrapped_lines)
#             start_y = popup_rect.centery - total_text_height // 2
            
#             for i, line in enumerate(wrapped_lines):
#                 text_surface = self.font.render(line, True, (0, 0, 0))
#                 text_rect = text_surface.get_rect(centerx=popup_rect.centerx, 
#                                                   top=start_y + i * line_height)
#                 self.screen.blit(text_surface, text_rect)
            
#             # Button text
#             btn_text = self.font.render("OK", True, (255, 255, 255))
#             btn_rect = btn_text.get_rect(center=button_rect.center)
#             self.screen.blit(btn_text, btn_rect)
            
#             pg.display.flip()
        
#     def wrap_text(text, font, max_width):
#             words = text.split()
#             lines = []
#             current_line = []
            
#             for word in words:
#                 test_line = ' '.join(current_line + [word])
#                 test_width, _ = font.size(test_line)
                
#                 if test_width <= max_width:
#                     current_line.append(word)
#                 else:
#                     lines.append(' '.join(current_line))
#                     current_line = [word]
            
#             if current_line:
#                 lines.append(' '.join(current_line))
            
#             return lines

    
    
    
    
    
    
    
    
#     def set_mission(self, mission_text):

#         self.current_mission = mission_text
#         self.mission_completed = False
#         self.turret_upgraded_first_time = False
#         self.gold_reward_given = False

#     def check_turret_upgrade_mission(self, turret_group):
     
#         # Check if a turret has been upgraded for the first time
#         if not self.turret_upgraded_first_time:
#             for tower in turret_group:
#                 # Assuming the tower has an upgrade_level attribute
#                 if tower.upgrade_turret > 1:
#                     self.turret_upgraded_first_time = True
#                     self.show_popup("Congratulations! You've earned 300 gold for upgrading a tower.")
#                     self.current_mission=""
#                     return True
#             return False

#     def render_mission(self):
       
#         if not self.current_mission:
#             return

#         # Create a transparent surface
#         mission_surface = pg.Surface((300, 50), pg.SRCALPHA)
#         mission_surface.fill((100, 100, 100, 100))  # Semi-transparent gray

#         # Render mission text
#         mission_text = f"Mission: {self.current_mission}"
#         text_color = (255, 255, 255)  # White for ongoing

#         text_render = self.font.render(mission_text, True, text_color)
#         text_rect = text_render.get_rect(topleft=(10, 10))
        
#         # Blit the transparent background
#         self.screen.blit(mission_surface, (0, 0))
        
#         # Blit the mission text
#         self.screen.blit(text_render, text_rect)
import pygame as pg

class StoryScene:
    def __init__(self, screen, font, button_text="Start Mission"):
        self.screen = screen
        self.font = font
        self.button_text = button_text
        self.setup_dimensions()
        self.finished = False

    def setup_dimensions(self):
        self.screen_width, self.screen_height = self.screen.get_size()
        self.popup_width = self.screen_width - 40
        self.popup_height = self.screen_height - 100
        self.popup_x = (self.screen_width - self.popup_width) // 2
        self.popup_y = (self.screen_height - self.popup_height) // 2
        self.popup_rect = pg.Rect((self.popup_x, self.popup_y, self.popup_width, self.popup_height))
        self.button_rect = pg.Rect(
            self.popup_x + (self.popup_width - 180) // 2,
            self.popup_y + self.popup_height - 70,
            180, 50
        )

    def wrap_text(self, text, max_width):
        words = text.split()
        lines = []
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            if self.font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        return lines

    def draw(self, text):
        overlay = pg.Surface((self.screen_width, self.screen_height), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))

        pg.draw.rect(self.screen, (220, 220, 220), self.popup_rect, border_radius=10)
        pg.draw.rect(self.screen, (50, 150, 50), self.button_rect, border_radius=8)

        wrapped_lines = self.wrap_text(text, self.popup_width - 40)
        line_height = self.font.get_linesize()
        total_text_height = line_height * len(wrapped_lines)
        start_y = self.popup_rect.centery - total_text_height // 2

        for i, line in enumerate(wrapped_lines):
            text_surface = self.font.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(centerx=self.popup_rect.centerx, 
                                              top=start_y + i * line_height)
            self.screen.blit(text_surface, text_rect)

        btn_text = self.font.render(self.button_text, True, (255, 255, 255))
        btn_rect = btn_text.get_rect(center=self.button_rect.center)
        self.screen.blit(btn_text, btn_rect)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                self.finished = True

class MissionManager:
    def __init__(self):
        self.current_mission = ""
        self.mission_completed = False
        self.turret_upgraded_first_time = False
        self.gold_reward_given = False

    def set_mission(self, mission_text):
        self.current_mission = mission_text
        self.mission_completed = False
        self.turret_upgraded_first_time = False
        self.gold_reward_given = False

    def check_turret_upgrade_mission(self, turret_group):
        if not self.turret_upgraded_first_time:
            for tower in turret_group:
                if tower.upgrade_turret > 1:
                    self.turret_upgraded_first_time = True
                    self.current_mission = ""
                    return True
        return False

    def render_mission(self, screen, font):
        if not self.current_mission:
            return

        mission_surface = pg.Surface((300, 50), pg.SRCALPHA)
        mission_surface.fill((100, 100, 100, 100))

        mission_text = f"Mission: {self.current_mission}"
        text_render = font.render(mission_text, True, (255, 255, 255))
        text_rect = text_render.get_rect(topleft=(10, 10))

        screen.blit(mission_surface, (0, 0))
        screen.blit(text_render, text_rect)