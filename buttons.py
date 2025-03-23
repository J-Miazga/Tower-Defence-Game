import pygame as pg

class Button():
    def __init__(self, x, y, width, height, text, font, text_color=(255, 255, 255),
                 button_color=(50, 150, 50), hover_color=(70, 200, 70)):
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.button_color = button_color
        self.hover_color = hover_color

        # Prerender tekstu
        self.update_text_surface()
    
    def update_text_surface(self):
        # Update the text surface (needed if text or color changes)
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
    def draw(self, surface):
        # Sprawdza, czy myszka jest nad przyciskiem
        mouse_pos = pg.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse_pos)

        # Wybiera kolor w zależności od hovera
        color = self.hover_color if hovered else self.button_color

        # Rysuje prostokąt
        pg.draw.rect(surface, color, self.rect, border_radius=8)

        # Rysuje tekst (centrujemy względem recta)
        surface.blit(self.text_surface, self.text_rect)

    def is_clicked(self, event):
        # Sprawdza kliknięcie myszą wewnątrz recta
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    def set_text(self, new_text):
        # Update button text
        self.text = new_text
        self.update_text_surface()