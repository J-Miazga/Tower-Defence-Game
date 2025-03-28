import pygame as pg
import constant as cs
from turret_data import TURRET_DATA
import math
from logger import game_logger


class Turret(pg.sprite.Sprite):
    def __init__(self,pos,tower_type,tile_pos=None):
        pg.sprite.Sprite.__init__(self)
        self.turret_images={}
        self.load_tower_images() 
        self.tower_type=tower_type
        self.image = self.turret_images.get(tower_type)
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.center=pos
        self.upgrade_turret=1
        self.turret_index = self.get_turret_data_index()
        self.range=TURRET_DATA[self.turret_index].get("range")
        self.attack_speed=TURRET_DATA[self.turret_index].get("attack_speed")
        self.damage=TURRET_DATA[self.turret_index].get("damage")
        self.tile_pos = tile_pos
        self.range_image=pg.Surface((self.range*2,self.range*2))
        self.range_image.fill((0,0,0))
        self.range_image.set_colorkey((0,0,0))
        pg.draw.circle(self.range_image,"grey100",(self.range,self.range),self.range)
        self.range_image.set_alpha(100)
        self.range_rect=self.range_image.get_rect()
        self.range_rect.center=self.rect.center
        self.selected=False
        
        
        self.target = None
        self.last_fire_time = 0

              
    def load_tower_images(self):
        # Load all enemy images from your tiles directory
        tower_types = ['tower_1','tower_1_upgrade','tower_2','tower_2_upgrade','tower_3','tower_3_upgrade']
        for tower_type in tower_types:
            try:
                img_path = f"Sprites/towers/{tower_type}.png"
                self.turret_images[tower_type] = pg.image.load(img_path).convert_alpha()
            except:
                print(f"Could not load image for {tower_type}")
                # Create a colored placeholder doesnt work no tile size variabels
                placeholder = pg.Surface((cs.TILE_SIZE,cs.TILE_SIZE))
                placeholder.fill((0, 0, 0))
                self.turret_images[tower_type] = placeholder
    
    def delete_turret(self):
        self.kill()
    
    def get_turret_data_index(self):
        # Map turret types to their data indices
        if self.tower_type == "tower_1":
            return 0
        elif self.tower_type == "tower_2":
            return 2
        elif self.tower_type == "tower_3":
            return 4  # Using same data as tower_1 for now, you can add more in turret_data.py
        else:
            return 0  # Default to first turret data
    
    def check_line_of_sight(self, map_obj, enemy):
        """Check if there's a mountain blocking the line of sight"""
        # Get turret and enemy tile coordinates
        turret_tile_x = self.rect.centerx // map_obj.tile_size
        turret_tile_y = self.rect.centery // map_obj.tile_size
        enemy_tile_x = enemy.rect.centerx // map_obj.tile_size
        enemy_tile_y = enemy.rect.centery // map_obj.tile_size
        
        # Use Bresenham's line algorithm to check tiles between turret and enemy
        def get_line_tiles(x0, y0, x1, y1):
            tiles = []
            dx = abs(x1 - x0)
            dy = abs(y1 - y0)
            x, y = x0, y0
            sx = 1 if x0 < x1 else -1
            sy = 1 if y0 < y1 else -1
            
            if dx > dy:
                err = dx / 2.0
                while x != x1:
                    tiles.append((x, y))
                    err -= dy
                    if err < 0:
                        y += sy
                        err += dx
                    x += sx
            else:
                err = dy / 2.0
                while y != y1:
                    tiles.append((x, y))
                    err -= dx
                    if err < 0:
                        x += sx
                        err += dy
                    y += sy
            
            tiles.append((x1, y1))
            return tiles
        
        # Get tiles between turret and enemy
        line_tiles = get_line_tiles(turret_tile_x, turret_tile_y, enemy_tile_x, enemy_tile_y)
        
        # Skip first and last tiles (turret and enemy positions)
        for tile_x, tile_y in line_tiles[1:-1]:
            # Check if tile is within map bounds
            if 0 <= tile_x < map_obj.width and 0 <= tile_y < map_obj.height:
                # If any tile in the line is a mountain, block line of sight
                if map_obj.tiles[tile_y][tile_x].tile_type == 'mountain':
                    return False
        
        return True
    
    
    def find_target(self, enemy_group):
        """Find the enemy closest to the finish line within range"""
        closest_enemy = None
        closest_distance = float('inf')
        
        for enemy in enemy_group:
           if enemy.hp>0: # Calculate distance to enemy
                distance = math.sqrt(
                    (enemy.rect.centerx - self.rect.centerx)**2 + 
                    (enemy.rect.centery - self.rect.centery)**2
                )
                
                # Check if enemy is within range
                if distance <= self.range:
                    # Use path index to determine closeness to finish
                    # Lower path index means closer to finish
                    if closest_enemy is None or enemy.current_path_index > closest_enemy.current_path_index:
                        closest_enemy = enemy
                        closest_distance = distance
        
        return closest_enemy

    def calculate_rotation_angle(self, target):
        """Calculate the correct rotation angle"""
        # Calculate the vector from turret to target
        dx = target.rect.centerx - self.rect.centerx
        dy = target.rect.centery - self.rect.centery
        
        # Calculate angle in radians
        # Use atan2 to get the angle, then convert to degrees
        # Subtract 90 to align with the initial upward orientation
        angle = math.degrees(math.atan2(-dy, dx))-90
        
        return angle
        
    def update(self, enemy_group):
        """Update turret targeting and firing"""
        current_time = pg.time.get_ticks()
        
        # Find the target
        self.target = self.find_target(enemy_group)
        
        # Check if enough time has passed since last fire
        if current_time - self.last_fire_time >= self.attack_speed:
            # If target found, rotate and fire
            if self.target:
                # Calculate rotation angle
                angle = self.calculate_rotation_angle(self.target)
                
                # Rotate image
                self.image = pg.transform.rotate(self.original_image, angle)
                self.rect = self.image.get_rect(center=self.rect.center)
                
                
                if self.check_line_of_sight(self.target.map, self.target):
                    # Fire at the target
                    self.target.hp -= self.damage
                    game_logger.log(f"{self.tower_type} hit enemy at {self.target.rect.center}, remaining HP: {self.target.hp}","info")
                # Update last fire time
                self.last_fire_time = current_time
    
    def upgrade(self):
        self.upgrade_turret+=1
        self.tower_type=f"{self.tower_type}_upgrade"
        self.turret_index = self.get_turret_data_index()
        self.range=TURRET_DATA[self.turret_index+1].get("range")
        self.attack_speed=TURRET_DATA[self.turret_index+1].get("attack_speed")
        self.damage=TURRET_DATA[self.turret_index+1].get("damage")
        print(self.range,self.attack_speed,self.damage)
        self.range_image=pg.Surface((self.range*2,self.range*2))
        self.range_image.fill((0,0,0))
        self.range_image.set_colorkey((0,0,0))
        pg.draw.circle(self.range_image,"grey100",(self.range,self.range),self.range)
        self.range_image.set_alpha(100)
        self.range_rect=self.range_image.get_rect()
        self.range_rect.center=self.rect.center
        self.image=self.turret_images[self.tower_type]
        self.original_image=self.image.copy()

    def draw(self,surface):
        surface.blit(self.image,self.rect)
        if self.selected:
            surface.blit(self.range_image,self.range_rect)
   

   