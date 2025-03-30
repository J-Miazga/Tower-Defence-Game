import pygame as pg
from tiles import Tile
import constant as cs
from enemy_data import ENEMY_SPAWN_DATA
from logger import game_logger

class Map:
    def __init__(self, tile_size=cs.TILE_SIZE):
        # Basic map state and properties
        self.level = 1
        self.tile_size = tile_size
        self.tiles = []  # 2D list of Tile objects
        self.tile_images = {}  # Mapping of tile type to its image
        self.load_tile_images()  # Load all tile graphics
        self.tile_group = pg.sprite.Group()  # For rendering efficiency
        self.hp = cs.HEALTH
        self.money = cs.MONEY
        self.width = 0  # Determined after loading a map
        self.height = 0
        self.enemy_list = []  # Sequence of enemies to spawn
        self.spawned_enemy = 0
        self.enemies_killed = 0
        self.enemies_missed = 0

    def load_tile_images(self):
        """
        Load tile graphics from disk. If not found, use a placeholder.
        """
        tile_types = ['grass', 'path', 'mountain', 'forest', 'marsh', 'start', 'finish']
        for tile_type in tile_types:
            try:
                img_path = f"Sprites/tiles/{tile_type}.png"
                self.tile_images[tile_type] = pg.image.load(img_path).convert_alpha()
            except:
                game_logger.log(f"Could not load image for {tile_type}", "error")
                placeholder = pg.Surface((self.tile_size, self.tile_size))
                placeholder.fill((0, 0, 0))
                self.tile_images[tile_type] = placeholder

    def level_finished(self):
        """
        Return True if all enemies have been processed (killed or missed).
        """
        return (self.enemies_killed + self.enemies_missed) >= len(self.enemy_list)

    def generate_enemy_list(self):
        """
        Populate enemy_list based on current level’s spawn data.
        """
        enemies = ENEMY_SPAWN_DATA[self.level - 1]
        for enemy_type, count in enemies.items():
            for _ in range(count):
                self.enemy_list.append(enemy_type)

    def reset_level(self):
        """
        Reset map state to prepare for a new level.
        """
        self.enemies_killed = 0
        self.enemies_missed = 0
        self.enemy_list = []
        self.spawned_enemy = 0

    def load_from_file(self, filename):
        """
        Load tile layout from a txt map file.
        """
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
        """
        Clear all existing tiles and sprite groups.
        """
        self.tiles = []
        self.tile_group.empty()

    def read_map_file(self, filename):
        """
        Read map file into a 2D list of tile type strings.
        """
        map_data = []
        with open(filename, 'r') as file:
            for line in file:
                row = line.strip().split(',')
                map_data.append(row)
        return map_data

    def build_tiles_from_data(self, map_data):
        """
        Convert tile type strings into Tile objects and build the map grid.
        """
        for y in range(self.height):
            row = []
            for x in range(len(map_data[y])):
                tile_type = map_data[y][x]
                tile = self.create_tile(x, y, tile_type)
                row.append(tile)
                self.tile_group.add(tile)
            self.tiles.append(row)

    def create_tile(self, x, y, tile_type):
        """
        Create a tile of a specific type at a specific grid position.
        If tile type is unknown, use a fallback grass tile.
        """
        if tile_type in self.tile_images:
            return Tile(x * self.tile_size, y * self.tile_size, self.tile_images[tile_type], tile_type)
        else:
            game_logger.log(f"Unknown tile type: {tile_type}", "warning")
            return Tile(x * self.tile_size, y * self.tile_size, self.tile_images['grass'], 'grass')

    def get_tile_at_position(self, x, y):
        """
        Given pixel coordinates, return the tile at that location.
        """
        tile_x = x // self.tile_size
        tile_y = y // self.tile_size
        if 0 <= tile_x < self.width and 0 <= tile_y < self.height:
            return self.tiles[tile_y][tile_x]
        return None

    def draw(self, surface):
        """
        Draw the full map using its sprite group.
        """
        self.tile_group.draw(surface)
