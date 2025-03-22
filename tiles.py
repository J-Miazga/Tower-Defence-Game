import pygame as pg

class Tile(pg.sprite.Sprite):
    def __init__(self, x, y, image, tile_type):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tile_type = tile_type
    def get_movement_cost(self):
        # Different terrain types have different movement costs
        costs = {
            'path': 1.0,      # Normal movement
            'start': 1.0,     # Normal movement at start
            'finish': 1.0,    # Normal movement at finish
            'marsh': 2.0,     # Slower through marsh
            'grass': float('inf'),  # Cannot move on grass
            'forest': float('inf'), # Cannot move on forest
            'mountain': float('inf')  # Cannot move on mountain
        }
        return costs.get(self.tile_type, float('inf'))