import pygame as pg

class Tile(pg.sprite.Sprite):
    def __init__(self, x, y, image, tile_type):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tile_type = tile_type
    def get_movement_cost(self,enemy_type):
        costs = {
            'path': 1.0,     
            'start': 1.0,     
            'finish': 1.0,    
            'marsh': 2.0,     
            'grass': float('inf'),  
            'forest': float('inf'), 
            'mountain': float('inf')  
        }
        if self.tile_type == 'marsh' and enemy_type == 'fast':
            return 1.0
        return costs.get(self.tile_type, float('inf'))