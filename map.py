import pygame as pg
from tiles import Tile
import constant as cs
from enemy_data import ENEMY_SPAWN_DATA
from logger import game_logger

class Map:
    def __init__(self, tile_size=cs.TILE_SIZE):
        self.level=1
        self.tile_size = tile_size
        self.tiles = []
        self.tile_images = {}
        self.load_tile_images()
        self.tile_group = pg.sprite.Group()
        self.hp=cs.HEALTH
        self.money=cs.MONEY
        self.width = 0  # Will be determined by loaded map
        self.height = 0  # Will be determined by loaded map
        self.enemy_list=[]
        self.spawned_enemy=0
        self.enemies_killed=0
        self.enemies_missed=0
        
    def load_tile_images(self):
        tile_types = ['grass', 'path', 'mountain','forest','marsh','start','finish']
        for tile_type in tile_types:
            try:
                img_path = f"Sprites/tiles/{tile_type}.png"
                self.tile_images[tile_type] = pg.image.load(img_path).convert_alpha()
            except:
                game_logger.log(f"Could not load image for {tile_type}","error")
                placeholder = pg.Surface((self.tile_size, self.tile_size))
                placeholder.fill((0, 0, 0))
                self.tile_images[tile_type] = placeholder


    def level_finished(self):
        return (self.enemies_killed + self.enemies_missed) >= len(self.enemy_list)

    
    def generate_enemy_list(self):
        enemies=ENEMY_SPAWN_DATA[self.level-1]
        for enemy_type in enemies:
            enemies_to_spawn=enemies[enemy_type]
            for enemy in range(enemies_to_spawn):
                self.enemy_list.append(enemy_type)
    
    def reset_level(self):
        self.enemies_killed=0
        self.enemies_missed=0
        self.enemy_list=[]  
        self.spawned_enemy=0  
    
    def load_from_file(self, filename):
        self.clear_map()
        try:
            map_data = self.read_map_file(filename)
            self.height = len(map_data)
            self.width = len(map_data[0]) if self.height > 0 else 0
            self.build_tiles_from_data(map_data)
            return True
        except Exception as e:
            game_logger.log(f"Error loading map from {filename}: {e}", "error")
            return False

    def clear_map(self):
        self.tiles = []
        self.tile_group.empty()

    def read_map_file(self, filename):
        map_data = []
        with open(filename, 'r') as file:
            for line in file:
                row = line.strip().split(',')
                map_data.append(row)
        return map_data

    def build_tiles_from_data(self, map_data):
        for y in range(self.height):
            row = []
            for x in range(len(map_data[y])):
                tile_type = map_data[y][x]
                tile = self.create_tile(x, y, tile_type)
                row.append(tile)
                self.tile_group.add(tile)
            self.tiles.append(row)

    def create_tile(self, x, y, tile_type):
        if tile_type in self.tile_images:
            return Tile(x * self.tile_size, y * self.tile_size, self.tile_images[tile_type], tile_type)
        else:
            game_logger.log(f"Unknown tile type: {tile_type}", "warning")
            return Tile(x * self.tile_size, y * self.tile_size, self.tile_images['grass'], 'grass')
    
    def get_tile_at_position(self, x, y):
        tile_x = x // self.tile_size
        tile_y = y // self.tile_size
        if 0 <= tile_x < self.width and 0 <= tile_y < self.height:
            return self.tiles[tile_y][tile_x]
        return None
    
    def draw(self, surface):
        self.tile_group.draw(surface)
    
  