import pygame as pg
import constant as cs
from turret_data import TURRET_DATA
import math
from logger import game_logger

class Turret(pg.sprite.Sprite):
    turret_images = {}  # Klasa trzyma obrazki wspólne dla wszystkich wieżyczek

    def __init__(self, pos, tower_type, tile_pos=None):
        pg.sprite.Sprite.__init__(self)
        Turret.load_tower_images()  # Ładowanie tylko raz
        self.tower_type = tower_type
        self.image = Turret.turret_images.get(tower_type)
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.upgrade_turret = 1
        self.range = TURRET_DATA[self.tower_type]["range"]
        self.attack_speed = TURRET_DATA[self.tower_type]["attack_speed"]
        self.damage = TURRET_DATA[self.tower_type]["damage"]
        self.tile_pos = tile_pos
        
        self.range_image = self.create_range_image(self.range)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center
        self.selected = False
        self.target = None
        self.last_fire_time = 0

    @classmethod
    def load_tower_images(cls):
        if cls.turret_images:
            return
        tower_types = ['tower_1', 'tower_1_upgrade', 'tower_2', 'tower_2_upgrade', 'tower_3', 'tower_3_upgrade']
        for tower_type in tower_types:
            try:
                img_path = f"Sprites/towers/{tower_type}.png"
                cls.turret_images[tower_type] = pg.image.load(img_path).convert_alpha()
            except:
                print(f"Could not load image for {tower_type}")
                placeholder = pg.Surface((cs.TILE_SIZE, cs.TILE_SIZE))
                placeholder.fill((0, 0, 0))
                cls.turret_images[tower_type] = placeholder

    def delete_turret(self):
        self.kill()

    def check_line_of_sight(self, map_obj, enemy):
        turret_tile_x = self.rect.centerx // map_obj.tile_size
        turret_tile_y = self.rect.centery // map_obj.tile_size
        enemy_tile_x = enemy.rect.centerx // map_obj.tile_size
        enemy_tile_y = enemy.rect.centery // map_obj.tile_size

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

        line_tiles = get_line_tiles(turret_tile_x, turret_tile_y, enemy_tile_x, enemy_tile_y)

        for tile_x, tile_y in line_tiles[1:-1]:
            if 0 <= tile_x < map_obj.width and 0 <= tile_y < map_obj.height:
                if map_obj.tiles[tile_y][tile_x].tile_type == 'mountain':
                    return False

        return True

    def create_range_image(self, radius):
        surface = pg.Surface((radius * 2, radius * 2))
        surface.fill((0, 0, 0))
        surface.set_colorkey((0, 0, 0))
        pg.draw.circle(surface, "grey100", (radius, radius), radius)
        surface.set_alpha(100)
        return surface

    def find_target(self, enemy_group):
        closest_enemy = None

        for enemy in enemy_group:
            if enemy.hp > 0:
                distance = math.sqrt(
                    (enemy.rect.centerx - self.rect.centerx)**2 + 
                    (enemy.rect.centery - self.rect.centery)**2
                )
                if distance <= self.range:
                    if closest_enemy is None or enemy.current_path_index > closest_enemy.current_path_index:
                        closest_enemy = enemy
                        

        return closest_enemy

    def calculate_rotation_angle(self, target):
        dx = target.rect.centerx - self.rect.centerx
        dy = target.rect.centery - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx)) - 90
        return angle

    def update(self, enemy_group):
        current_time = pg.time.get_ticks()

        if current_time - self.last_fire_time < self.attack_speed:
            return  # jeszcze nie czas na strzał

        self.target = self.find_target(enemy_group)
        if not self.target:
            return  # brak celu

        if not self.check_line_of_sight(self.target.map, self.target):
            return  # brak linii strzału

        # Obrót wieżyczki
        angle = self.calculate_rotation_angle(self.target)
        self.image = pg.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # Zadanie obrażeń
        self.target.hp -= self.damage
        game_logger.log(f"{self.tower_type} hit enemy at {self.target.rect.center}, remaining HP: {self.target.hp}","info")
        self.last_fire_time = current_time


    def upgrade(self):
        self.upgrade_turret += 1
        self.tower_type = f"{self.tower_type}_upgrade"
        self.range = TURRET_DATA[self.tower_type]["range"]
        self.attack_speed = TURRET_DATA[self.tower_type]["attack_speed"]
        self.damage = TURRET_DATA[self.tower_type]["damage"]
        self.range_image = self.create_range_image(self.range)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center
        self.image = Turret.turret_images[self.tower_type]
        self.original_image = self.image.copy()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)

   