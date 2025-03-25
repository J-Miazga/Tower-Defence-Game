import pygame as pg
import constant as cs
from turret_data import TURRET_DATA
import math

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
        self.range=TURRET_DATA[self.upgrade_turret-1].get("range")
        self.attack_speed=TURRET_DATA[self.upgrade_turret-1].get("attack_speed")
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
            return 1
        elif self.tower_type == "tower_3":
            return 2  # Using same data as tower_1 for now, you can add more in turret_data.py
        else:
            return 0  # Default to first turret data
    
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
                
                # Fire at the target
                #print(f"{self.tower_type} turret fired at enemy. Enemy HP: {self.target.hp}")
                
                # Damage the enemy
                self.target.hp -= 1  # Basic damage, you can modify this later
                
                # Update last fire time
                self.last_fire_time = current_time
    
    def upgrade(self):
        self.upgrade_turret+=1
        self.turret_index = self.get_turret_data_index()
        self.range=TURRET_DATA[self.turret_index].get("range")
        self.attack_speed=TURRET_DATA[self.turret_index].get("attack_speed")
        self.range_image=pg.Surface((self.range*2,self.range*2))
        self.range_image.fill((0,0,0))
        self.range_image.set_colorkey((0,0,0))
        pg.draw.circle(self.range_image,"grey100",(self.range,self.range),self.range)
        self.range_image.set_alpha(100)
        self.range_rect=self.range_image.get_rect()
        self.range_rect.center=self.rect.center
        self.image=self.turret_images[f"{self.tower_type}_upgrade"]
        self.original_image=self.image.copy()

    def draw(self,surface):
        surface.blit(self.image,self.rect)
        if self.selected:
            surface.blit(self.range_image,self.range_rect)
   