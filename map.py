import pygame as pg
from tiles import Tile
import constant as cs
from enemy_data import ENEMY_SPAWN_DATA

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
        # Load all tile images from your tiles directory
        tile_types = ['grass', 'path', 'mountain','forest','marsh','start','finish']
        for tile_type in tile_types:
            try:
                img_path = f"Sprites/tiles/{tile_type}.png"
                self.tile_images[tile_type] = pg.image.load(img_path).convert_alpha()
            except:
                print(f"Could not load image for {tile_type}")
                # Create a colored placeholder
                placeholder = pg.Surface((self.tile_size, self.tile_size))
                placeholder.fill((0, 0, 0))
                self.tile_images[tile_type] = placeholder

    def level_finished(self):
        if self.enemies_killed+self.enemies_missed==len(self.enemy_list):
            return True
    
    def process_enemies(self):
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
        # Clear existing tiles
        self.tiles = []
        self.tile_group.empty()
        
        try:
            with open(filename, 'r') as file:
                map_data = []
                for line in file:
                    row = line.strip().split(',')
                    map_data.append(row)
                
                self.height = len(map_data)
                self.width = len(map_data[0]) if self.height > 0 else 0
                
                # Create tile sprites based on map_data
                for y in range(self.height):
                    row = []
                    for x in range(len(map_data[y])):
                        tile_type = map_data[y][x]
                        if tile_type in self.tile_images:
                            tile = Tile(x * self.tile_size, y * self.tile_size, 
                                      self.tile_images[tile_type], tile_type)
                            row.append(tile)
                            self.tile_group.add(tile)
                        else:
                            print(f"Unknown tile type: {tile_type}")
                            # Add a default grass tile as fallback
                            tile = Tile(x * self.tile_size, y * self.tile_size, 
                                      self.tile_images['grass'], 'grass')
                            row.append(tile)
                            self.tile_group.add(tile)
                    self.tiles.append(row)
                return True
        except Exception as e:
            print(f"Error loading map from {filename}: {e}")
            return False
    
    def get_tile_at_position(self, x, y):
        # Get tile at pixel position
        tile_x = x // self.tile_size
        tile_y = y // self.tile_size
        if 0 <= tile_x < self.width and 0 <= tile_y < self.height:
            return self.tiles[tile_y][tile_x]
        return None
    
    def draw(self, surface):
        self.tile_group.draw(surface)
    
  