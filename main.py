import pygame as pg
import constant as cs
from enemies import Enemy
from map import Map
from tiles import Tile

pg.init()

clock=pg.time.Clock()
screen=pg.display.set_mode((1,1))
pg.display.set_caption("Tower Defense Game")

last_enemy_spawn=pg.time.get_ticks()

game_map = Map()
#map_loaded = game_map.load_from_file('maps/level1.txt')
#map_loaded = game_map.load_from_file('maps/level2.txt')
#map_loaded = game_map.load_from_file('maps/level3.txt')
map_loaded = game_map.load_from_file('maps/endless_level.txt')
if not map_loaded:
    print("Failed to load map!")
screen=pg.display.set_mode((game_map.width*cs.TILE_SIZE,game_map.height*cs.TILE_SIZE))
game_map.process_enemies()


enemy_group=pg.sprite.Group()



run=True
while run:
    
    clock.tick(cs.FPS)
    
    game_map.draw(screen)
    
    enemy_group.update()
    enemy_group.draw(screen)
    
    if pg.time.get_ticks()-last_enemy_spawn>cs.SPAWN_RATE:
        if game_map.spawned_enemy <len(game_map.enemy_list):
            enemy_type=game_map.enemy_list[game_map.spawned_enemy]
            enemy=Enemy(game_map,enemy_type)
            enemy_group.add(enemy)
            game_map.spawned_enemy+=1
            last_enemy_spawn=pg.time.get_ticks()
    
    for event in pg.event.get():
        
        if event.type==pg.QUIT:
            run=False
            
    pg.display.flip()
pg.quit()