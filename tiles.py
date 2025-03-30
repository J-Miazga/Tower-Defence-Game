import pygame as pg

class Tile(pg.sprite.Sprite):
    def __init__(self, x, y, image, tile_type):
        super().__init__()
        # Image to be rendered for the tile
        self.image = image
        # Position and size of the tile on screen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Type of terrain (e.g. path, grass, mountain)
        self.tile_type = tile_type

    def get_movement_cost(self, enemy_type):
        """
        Returns the movement cost for a tile based on its type and the enemy type.
        Lower values = faster movement. 'inf' means impassable.
        """
        costs = {
            'path': 1.0,           # Normal movement
            'start': 1.0,          # Spawn point
            'finish': 1.0,         # Goal point
            'marsh': 2.0,          # Slows most enemies
            'grass': float('inf'), # Cannot be walked on
            'forest': float('inf'),
            'mountain': float('inf')
        }

        # Exception: fast enemies ignore marsh penalty
        if self.tile_type == 'marsh' and enemy_type == 'fast':
            return 1.0

        # Return standard cost, or inf if unknown tile
        return costs.get(self.tile_type, float('inf'))
