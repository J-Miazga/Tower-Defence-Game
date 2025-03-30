import pygame as pg

class Button:
    def __init__(self, x, y, width, height, text, font, 
                 text_color=(255, 255, 255), 
                 button_color=(50, 150, 50), 
                 hover_color=(70, 200, 70)):
        # Initialize basic attributes and rectangle for positioning
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.button_color = button_color
        self.hover_color = hover_color

        # Pre-render text surface for efficiency
        self.update_text_surface()

    def update_text_surface(self):
        """Render the button's text and center it within the rect."""
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, surface):
        """Draw the button with hover effect and text on the given surface."""
        mouse_pos = pg.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse_pos)

        # Use hover color if mouse is over the button
        color = self.hover_color if hovered else self.button_color

        # Draw button background with rounded corners
        pg.draw.rect(surface, color, self.rect, border_radius=8)

        # Draw text centered in the button
        surface.blit(self.text_surface, self.text_rect)

    def is_clicked(self, event):
        """Check if the button was clicked with the left mouse button."""
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def set_text(self, new_text):
        """Update the button's text and re-render the surface."""
        self.text = new_text
        self.update_text_surface()
