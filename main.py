import pygame as pg
import constant as cs
from enemies import Enemy
from map import Map
from tiles import Tile

pg.init()

clock=pg.time.Clock()
screen=pg.display.set_mode((1,1))

game_map = Map()
map_loaded = game_map.load_from_file('maps/level1.txt')
#map_loaded = game_map.load_from_file('maps/level2.txt')
#map_loaded = game_map.load_from_file('maps/level3.txt')
#map_loaded = game_map.load_from_file('maps/endless_level.txt')
if not map_loaded:
    print("Failed to load map!")
screen=pg.display.set_mode((game_map.width*cs.TILE_SIZE,game_map.height*cs.TILE_SIZE))


pg.display.set_caption("Tower Defense Game")


enemy_image=pg.image.load('Sprites/enemies/enemy_1.png').convert_alpha()

enemy_group=pg.sprite.Group()
enemy=Enemy((200,300),enemy_image)

enemy_group.add(enemy)

run=True
while run:
    
    clock.tick(cs.FPS)
    
    game_map.draw(screen)
    
    enemy_group.update()
    enemy_group.draw(screen)
    
    for event in pg.event.get():
        
        if event.type==pg.QUIT:
            run=False
            
    pg.display.flip()
pg.quit()