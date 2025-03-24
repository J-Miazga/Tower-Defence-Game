# enemies.py
import pygame as pg
from map import Map
from pathfinding import a_star_search
import math
from enemy_data import ENEMY_DATA
import constant as cs

class Enemy(pg.sprite.Sprite):
    def __init__(self, map_obj,enemy_type):
        pg.sprite.Sprite.__init__(self)
        self.map = map_obj
        self.hp=ENEMY_DATA.get(enemy_type)["hp"]
        self.speed = ENEMY_DATA.get(enemy_type)["speed"]
        self.enemy_images={}
        self.load_enemy_images()
        self.path = []
        self.current_target = None
        self.current_path_index = 0
        self.image = self.enemy_images.get(enemy_type)
        self.rect = self.image.get_rect()
        self.original_image = self.image.copy()
        
        
        # Find start and finish tiles
        self.start_pos = self.find_tile_position('start')
        self.finish_pos = self.find_tile_position('finish')
        
        # Set initial position at start tile
        if self.start_pos:
            self.rect.center = (
                self.start_pos[0] * self.map.tile_size + self.map.tile_size // 2,
                self.start_pos[1] * self.map.tile_size + self.map.tile_size // 2
            )
            
            # Calculate path
            self.calculate_path(map_obj)
    
    def load_enemy_images(self):
        # Load all enemy images from your tiles directory
        enemy_types = ['normal','heavy','fast','boss']
        for enemy_type in enemy_types:
            try:
                img_path = f"Sprites/enemies/{enemy_type}.png"
                self.enemy_images[enemy_type] = pg.image.load(img_path).convert_alpha()
            except:
                print(f"Could not load image for {enemy_type}")
                # Create a colored placeholder doesnt work
                placeholder = pg.Surface((cs.TILE_SIZE,cs.TILE_SIZE))
                placeholder.fill((0, 0, 0))
                self.enemy_images[enemy_type] = placeholder
    
    def find_tile_position(self, tile_type):
        """Find the position of a specific tile type"""
        for y in range(self.map.height):
            for x in range(self.map.width):
                if self.map.tiles[y][x].tile_type == tile_type:
                    return (x, y)
        return None
    
    def calculate_path(self,map):
        """Calculate a path from start to finish"""
        if self.start_pos and self.finish_pos:
            self.path = a_star_search(self.map, self.start_pos, self.finish_pos)
            self.current_path_index = 0
            if self.path:
                self.set_next_target(map)
    
    def set_next_target(self,map):
        """Set the next target position from the path"""
        if self.current_path_index < len(self.path):
            next_tile = self.path[self.current_path_index]
            self.current_target = (
                next_tile[0] * self.map.tile_size + self.map.tile_size // 2,
                next_tile[1] * self.map.tile_size + self.map.tile_size // 2
            )
            self.current_path_index += 1
        else:
            map.hp-=1
            self.kill()
    
    def move(self,map):
        """Move towards the current target"""
        if self.current_target:
            dx = self.current_target[0] - self.rect.centerx
            dy = self.current_target[1] - self.rect.centery
            
            # Calculate direction
            distance = max(1, (dx**2 + dy**2)**0.5)  # Avoid division by zero
            dx = dx / distance * self.speed
            dy = dy / distance * self.speed
            
            self.rotate()
            # Move
            self.rect.x += dx
            self.rect.y += dy
            
            
            # Check if reached target
            if abs(self.rect.centerx - self.current_target[0]) < self.speed and \
               abs(self.rect.centery - self.current_target[1]) < self.speed:
                # Snap to target position
                self.rect.center = self.current_target
                # Set next target
                self.set_next_target(map)
    
    def rotate(self):
        #Rotate the enemy to face the direction of movement
        if self.current_target:
            # Calculate direction vector
            dx = self.current_target[0] - self.rect.centerx
            dy = self.current_target[1] - self.rect.centery
            
            # Calculate angle in radians and convert to degrees
            angle = math.degrees(math.atan2(-dy, dx))
            
            if hasattr(self, 'original_image'):
                # Rotate the original image to avoid quality loss from multiple rotations
                self.image = pg.transform.rotate(self.original_image, angle)
                # Update rect to maintain the center position
                self.rect = self.image.get_rect(center=self.rect.center)
    
    def update(self,map):
        self.move(map)
        if self.hp <=0:
            map.money+=cs.KILL_REWARD
            self.kill()