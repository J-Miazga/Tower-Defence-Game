import pygame as pg

class Tile(pg.sprite.Sprite):
    def __init__(self, x, y, image, tile_type):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tile_type = tile_type