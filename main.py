import pygame as pg
import constant as cs

pg.init()

clock=pg.time.Clock()

screen=pg.display.set_mode((cs.SCREEN_WIDTH,cs.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defense Game")
run=True
while run:
    
    clock.tick(cs.FPS)
    
    for event in pg.event.get():
        
        if event.type==pg.QUIT:
            run=False
pg.quit()