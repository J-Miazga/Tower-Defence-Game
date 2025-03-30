import pygame as pg
from map import Map
from pathfinding import a_star_search
import math
from enemy_data import ENEMY_DATA
import constant as cs

class Enemy(pg.sprite.Sprite):
    # Shared image dictionary for all enemy types (only loaded once)
    enemy_images = {}

    def __init__(self, map_obj, enemy_type):
        super().__init__()
        Enemy.load_enemy_images()  # Ensure images are loaded once
        self.image = Enemy.enemy_images.get(enemy_type)

        # Core enemy attributes
        self.map = map_obj
        enemy_stats = ENEMY_DATA[enemy_type]
        self.hp = enemy_stats["hp"]
        self.speed = enemy_stats["speed"]
        self.enemy_type = enemy_type

        self.path = []
        self.current_target = None
        self.current_path_index = 0

        self.rect = self.image.get_rect()
        self.original_image = self.image.copy()

        # Determine start and end points
        self.start_pos = self.find_tile_position('start')
        self.finish_pos = self.find_tile_position('finish')

        # Initialize position and path
        if self.start_pos:
            self.rect.center = (
                self.start_pos[0] * self.map.tile_size + self.map.tile_size // 2,
                self.start_pos[1] * self.map.tile_size + self.map.tile_size // 2
            )
            self.calculate_path()

    @classmethod
    def load_enemy_images(cls):
        """Load enemy sprites if not already loaded (shared across instances)."""
        if cls.enemy_images:
            return  # Already loaded

        enemy_types = ['normal', 'heavy', 'fast', 'boss']
        for enemy_type in enemy_types:
            try:
                img_path = f"Sprites/enemies/{enemy_type}.png"
                cls.enemy_images[enemy_type] = pg.image.load(img_path).convert_alpha()
            except:
                print(f"Could not load image for {enemy_type}")
                placeholder = pg.Surface((cs.TILE_SIZE, cs.TILE_SIZE))
                placeholder.fill((0, 0, 0))
                cls.enemy_images[enemy_type] = placeholder

    def find_tile_position(self, tile_type):
        """Locate a tile with a specific type (e.g., 'start', 'finish')."""
        for y in range(self.map.height):
            for x in range(self.map.width):
                if self.map.tiles[y][x].tile_type == tile_type:
                    return (x, y)
        return None

    def calculate_path(self):
        """Compute the A* path from start to goal."""
        if self.start_pos and self.finish_pos:
            self.path = a_star_search(self.map, self.start_pos, self.finish_pos, self.enemy_type)
            self.current_path_index = 0
            if self.path:
                self.set_next_target()

    def set_next_target(self):
        """Set the next position along the path for the enemy to move towards."""
        if self.current_path_index < len(self.path):
            next_tile = self.path[self.current_path_index]
            self.current_target = (
                next_tile[0] * self.map.tile_size + self.map.tile_size // 2,
                next_tile[1] * self.map.tile_size + self.map.tile_size // 2
            )
            self.current_path_index += 1
        else:
            # Enemy reached the goal
            self.map.hp -= 1
            self.map.enemies_missed += 1
            self.kill()

    def move(self):
        """Move enemy toward current target tile and rotate sprite appropriately."""
        if not self.current_target:
            return

        # Direction vector to target
        direction = pg.math.Vector2(self.current_target) - pg.math.Vector2(self.rect.center)
        distance = direction.length()
        if distance != 0:
            direction.normalize_ip()

        # Get current tile and calculate terrain effect
        current_tile_x, current_tile_y = self.path[self.current_path_index - 1]
        current_tile = self.map.tiles[current_tile_y][current_tile_x]
        movement_multiplier = 0.5 if current_tile.tile_type == 'marsh' and self.enemy_type != 'fast' else 1.0

        # Calculate movement vector
        movement = direction * self.speed * movement_multiplier

        # Rotate sprite
        angle = math.degrees(math.atan2(-direction.y, direction.x))
        self.image = pg.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # Move sprite
        self.rect.x += movement.x
        self.rect.y += movement.y

        # If close enough to the target tile, snap to center and advance
        if pg.math.Vector2(self.rect.center).distance_to(self.current_target) < self.speed:
            self.rect.center = self.current_target
            self.set_next_target()

    def update(self):
        """Update enemy each frame: move and handle death."""
        self.move()
        if self.hp <= 0:
            self.map.enemies_killed += 1
            self.map.money += cs.KILL_REWARD
            self.kill()
