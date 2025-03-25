# import pygame as pg
# import constant as cs
# from enemies import Enemy
# from map import Map
# from tiles import Tile
# from turrets import Turret
# from buttons import Button

# pg.init()

# clock=pg.time.Clock()
# screen=pg.display.set_mode((1,1))
# pg.display.set_caption("Tower Defense Game")

# last_enemy_spawn=pg.time.get_ticks()

# game_map = Map()
# map_loaded = game_map.load_from_file('maps/level1.txt')
# #map_loaded = game_map.load_from_file('maps/level2.txt')
# #map_loaded = game_map.load_from_file('maps/level3.txt')
# #map_loaded = game_map.load_from_file('maps/endless_level.txt')
# if not map_loaded:
#     print("Failed to load map!")
# screen=pg.display.set_mode((game_map.width*cs.TILE_SIZE+cs.SIDE_PANEL,game_map.height*cs.TILE_SIZE))
# game_map.process_enemies()

# text_font=pg.font.SysFont("Consolas",24,bold=True)

# enemy_group=pg.sprite.Group()
# turret_group=pg.sprite.Group()

# DEFAULT_BUTTON_COLOR = (50, 150, 50)      # Green
# SELECTED_BUTTON_COLOR = (100, 100, 255)   # Blue
# HOVER_COLOR = (70, 200, 70) 

# upgrade_button=Button(game_map.width*cs.TILE_SIZE+75,60,150,50,"Upgrade turret",pg.font.SysFont(None, 30))
# buy_turret_button=Button(game_map.width*cs.TILE_SIZE+75,120,150,50,"Buy turret",pg.font.SysFont(None, 30))
# cancel_button=Button(game_map.width*cs.TILE_SIZE+75,300,150,50,"Cancel",pg.font.SysFont(None, 30))
# start_wave_button=Button(game_map.width*cs.TILE_SIZE+75,400,150,50,"Start wave",pg.font.SysFont(None, 30))

# turret1_button=Button(game_map.width*cs.TILE_SIZE+25,180,100,40,"Tower 1",pg.font.SysFont(None, 24), button_color=SELECTED_BUTTON_COLOR)
# turret2_button=Button(game_map.width*cs.TILE_SIZE+135,180,100,40,"Tower 2",pg.font.SysFont(None, 24))
# turret3_button=Button(game_map.width*cs.TILE_SIZE+75,230,100,40,"Tower 3",pg.font.SysFont(None, 24))

# placing_turrets=False
# selected_turret=None
# selected_turret_type="tower_1"
# level_started=False
# game_over=False
# game_outcome=0

# def update_turret_button_colors():
#     # Reset all to default
#     turret1_button.button_color = DEFAULT_BUTTON_COLOR
#     turret2_button.button_color = DEFAULT_BUTTON_COLOR
#     turret3_button.button_color = DEFAULT_BUTTON_COLOR
    
#     # Set selected one to the selected color
#     if selected_turret_type == "tower_1":
#         turret1_button.button_color = SELECTED_BUTTON_COLOR
#     elif selected_turret_type == "tower_2":
#         turret2_button.button_color = SELECTED_BUTTON_COLOR
#     elif selected_turret_type == "tower_3":
#         turret3_button.button_color = SELECTED_BUTTON_COLOR

# def draw_text(text,font,text_col,x,y):
#     img=font.render(text,True,text_col)
#     screen.blit(img,(x,y))
# # Set initial button colors
# update_turret_button_colors()

# run=True
# while run:
    
#     clock.tick(cs.FPS)
#     screen.fill("grey100")
    
#     if not game_over:
#         if game_map.hp<=0:
#             game_over=True
#             game_outcome=-1
#         enemy_group.update(game_map)
#         for turret in turret_group:
#             turret.update(enemy_group)
    
#         game_map.draw(screen)
#         for turret in turret_group:
#             turret.draw(screen)
#         enemy_group.draw(screen)
    
#         draw_text(str(game_map.hp),text_font,"black",game_map.width*cs.TILE_SIZE+10,0)
#         draw_text(str(game_map.money),text_font,"black",game_map.width*cs.TILE_SIZE+100,0)
#         buy_turret_button.draw(screen)
#     else:
#         draw_text("You lost",text_font,"black",500,200) if game_outcome==-1 else draw_text("You won",text_font,"black",500,200)
#     if not game_over:
#         if placing_turrets:  
#             turret1_button.draw(screen)
#             turret2_button.draw(screen)
#             turret3_button.draw(screen)
#             cancel_button.draw(screen)

#         if selected_turret and not placing_turrets and selected_turret.upgrade_turret < cs.TURRET_MAX_LEVEL:
#             upgrade_button.draw(screen)
#         if not level_started:
#             start_wave_button.draw(screen)
#         else:
#             if pg.time.get_ticks()-last_enemy_spawn>cs.SPAWN_RATE:
#                 if game_map.spawned_enemy <len(game_map.enemy_list):
#                     enemy_type=game_map.enemy_list[game_map.spawned_enemy]
#                     enemy=Enemy(game_map,enemy_type)
#                     enemy_group.add(enemy)
#                     game_map.spawned_enemy+=1
#                     last_enemy_spawn=pg.time.get_ticks()
        
#         if game_map.level_finished():
#             level_started=False
#             if game_map.level==3:
#                 game_over=True
#                 game_outcome=1
#             game_map.level+=1
#             last_enemy_spawn=pg.time.get_ticks()
#             game_map.reset_level()
#             game_map.process_enemies()
#             game_map.money+=cs.LEVEL_COMPLETE_REWARD
    
#     for event in pg.event.get():
        
#         if event.type==pg.QUIT:
#             run=False
        
#         if buy_turret_button.is_clicked(event):
#             placing_turrets=True
        
#         if start_wave_button.is_clicked(event):
#             level_started=True
            
#         if placing_turrets:
#             if turret1_button.is_clicked(event):
#                 selected_turret_type = "tower_1"
#                 update_turret_button_colors()
#             elif turret2_button.is_clicked(event):
#                 selected_turret_type = "tower_2"
#                 update_turret_button_colors()
#             elif turret3_button.is_clicked(event):
#                 selected_turret_type = "tower_3"
#                 update_turret_button_colors()
        
#         if cancel_button.is_clicked(event):
#             placing_turrets=False
        
#         if upgrade_button.is_clicked(event) and selected_turret and selected_turret.upgrade_turret < cs.TURRET_MAX_LEVEL and not placing_turrets and game_map.money>=cs.UPGRADE_COST:
#             selected_turret.upgrade()
        
        
#     if event.type==pg.MOUSEBUTTONDOWN and event.button==1:
#         mouse_pos=pg.mouse.get_pos()
#         # Check if click is within map boundaries
#         if mouse_pos[0] < game_map.width * cs.TILE_SIZE and mouse_pos[1] < game_map.height * cs.TILE_SIZE:
#             # First check if we clicked on a turret
#             turret_clicked = False
#             for turret in turret_group:
#                 if turret.rect.collidepoint(mouse_pos):
#                     # Select this turret
#                     for t in turret_group:
#                         t.selected = False  # Deselect all other turrets
#                     turret.selected = True
#                     selected_turret = turret
#                     turret_clicked = True
#                     break
            
#             # If we didn't click on a turret, handle other cases
#             if not turret_clicked:
#                 # Deselect all turrets when clicking elsewhere
#                 for turret in turret_group:
#                     turret.selected = False
#                 selected_turret = None
                
#                 # Handle turret placement if we're in placement mode
#                 if placing_turrets:
#                     # Get the tile at the clicked position
#                     clicked_tile = game_map.get_tile_at_position(mouse_pos[0], mouse_pos[1])
            
#                     # Check if tile is valid for turret placement (grass tiles only)
#                     if clicked_tile and clicked_tile.tile_type == 'grass':
#                         # Check if there's already a turret on this tile
#                         tile_center = (clicked_tile.rect.centerx, clicked_tile.rect.centery)
                        
#                         # Check for existing turrets at this position
#                         turret_exists = False
#                         for turret in turret_group:
#                             if turret.tile_pos == (clicked_tile.rect.x // cs.TILE_SIZE, clicked_tile.rect.y // cs.TILE_SIZE):
#                                 turret_exists = True
#                                 break
                        
#                         # Place turret if none exists at this position
#                         if not turret_exists and game_map.money>=cs.BUY_COST:
#                             turret = Turret(tile_center, selected_turret_type, tile_pos=(clicked_tile.rect.x // cs.TILE_SIZE, clicked_tile.rect.y // cs.TILE_SIZE))
#                             turret_group.add(turret)
#                             game_map.money-=cs.BUY_COST
            
#     pg.display.flip()
# pg.quit()
import pygame as pg
import constant as cs
from enemies import Enemy
from map import Map
from tiles import Tile
from turrets import Turret
from buttons import Button
from enemy_data import ENEMY_SPAWN_DATA

pg.init()

font = pg.font.SysFont(None, 36)

def show_popup(surface, message):
    popup_width = 400
    popup_height = 200
    popup_rect = pg.Rect((120, 140, popup_width, popup_height))
    button_rect = pg.Rect((270, 260, 100, 40))
    
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    running = False  # ZAMKNIJ popup

        # Ciemne tło
        surface.fill((0, 0, 0))
        
        # Prostokąt popupu
        pg.draw.rect(surface, (220, 220, 220), popup_rect, border_radius=10)
        pg.draw.rect(surface, (50, 150, 50), button_rect, border_radius=8)

        # Tekst popupu
        text_surface = font.render(message, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(popup_rect.centerx, popup_rect.centery - 30))
        surface.blit(text_surface, text_rect)

        # Tekst przycisku
        btn_text = font.render("OK", True, (255, 255, 255))
        btn_rect = btn_text.get_rect(center=button_rect.center)
        surface.blit(btn_text, btn_rect)

        pg.display.flip()

def draw_text(text, font, text_col, x, y, surface):
    img = font.render(text, True, text_col)
    surface.blit(img, (x, y))

def show_mode_selection_menu():
    # Create a screen for the menu
    menu_screen = pg.display.set_mode((400, 300))
    pg.display.set_caption("Game Mode Selection")
    
    # Fonts
    title_font = pg.font.SysFont("Consolas", 36, bold=True)
    button_font = pg.font.SysFont("Consolas", 24)
    
    # Buttons
    endless_button = Button(100, 150, 200, 50, "Endless Wave", button_font)
    plot_button = Button(100, 220, 200, 50, "Plot Mode", button_font)
    
    # Menu loop
    while True:
        menu_screen.fill("grey100")
        
        # Draw title
        draw_text("Select Game Mode", title_font, "black", 80, 50, menu_screen)
        
        # Draw buttons
        endless_button.draw(menu_screen)
        plot_button.draw(menu_screen)
        
        # Event handling
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return None
            
            if endless_button.is_clicked(event):
                return 'endless'
            
            if plot_button.is_clicked(event):
                return 'plot'
        
        pg.display.flip()

def main(game_mode):
    # Main game logic, similar to your existing code
    clock = pg.time.Clock()
    screen = pg.display.set_mode((1,1))
    pg.display.set_caption("Tower Defense Game")

    last_enemy_spawn = pg.time.get_ticks()

    game_map = Map()
    
    # Select map based on game mode
    if game_mode == 'endless':
        map_loaded = game_map.load_from_file('maps/endless_level.txt')
        game_map.level=4
    else:  # plot mode
        map_loaded = game_map.load_from_file('maps/level1.txt')
    
    if not map_loaded:
        print("Failed to load map!")
        return

    screen = pg.display.set_mode((game_map.width*cs.TILE_SIZE+cs.SIDE_PANEL, game_map.height*cs.TILE_SIZE))
    show_popup(screen, "To jest popup!")
    game_map.process_enemies()

    text_font = pg.font.SysFont("Consolas", 24, bold=True)

    enemy_group = pg.sprite.Group()
    turret_group = pg.sprite.Group()

    DEFAULT_BUTTON_COLOR = (50, 150, 50)      # Green
    SELECTED_BUTTON_COLOR = (100, 100, 255)   # Blue
    HOVER_COLOR = (70, 200, 70) 

    upgrade_button = Button(game_map.width*cs.TILE_SIZE+75, 60, 150, 50, "Upgrade turret", pg.font.SysFont(None, 30))
    buy_turret_button = Button(game_map.width*cs.TILE_SIZE+75, 120, 150, 50, "Buy turret", pg.font.SysFont(None, 30))
    cancel_button = Button(game_map.width*cs.TILE_SIZE+75, 300, 150, 50, "Cancel", pg.font.SysFont(None, 30))
    start_wave_button = Button(game_map.width*cs.TILE_SIZE+75, 400, 150, 50, "Start wave", pg.font.SysFont(None, 30))

    turret1_button = Button(game_map.width*cs.TILE_SIZE+25, 180, 100, 40, "Tower 1", pg.font.SysFont(None, 24), button_color=SELECTED_BUTTON_COLOR)
    turret2_button = Button(game_map.width*cs.TILE_SIZE+135, 180, 100, 40, "Tower 2", pg.font.SysFont(None, 24))
    turret3_button = Button(game_map.width*cs.TILE_SIZE+75, 230, 100, 40, "Tower 3", pg.font.SysFont(None, 24))

    placing_turrets = False
    selected_turret = None
    selected_turret_type = "tower_1"
    level_started = False
    game_over = False
    game_outcome = 0

    def update_turret_button_colors():
        # Reset all to default
        turret1_button.button_color = DEFAULT_BUTTON_COLOR
        turret2_button.button_color = DEFAULT_BUTTON_COLOR
        turret3_button.button_color = DEFAULT_BUTTON_COLOR
        
        # Set selected one to the selected color
        if selected_turret_type == "tower_1":
            turret1_button.button_color = SELECTED_BUTTON_COLOR
        elif selected_turret_type == "tower_2":
            turret2_button.button_color = SELECTED_BUTTON_COLOR
        elif selected_turret_type == "tower_3":
            turret3_button.button_color = SELECTED_BUTTON_COLOR

    # Set initial button colors
    update_turret_button_colors()

    run = True
    while run:
        clock.tick(cs.FPS)
        screen.fill("grey100")
        
        if not game_over:
            if game_map.hp <= 0:
                game_over = True
                game_outcome = -1
            
            enemy_group.update(game_map)
            for turret in turret_group:
                turret.update(enemy_group)
        
            game_map.draw(screen)
            for turret in turret_group:
                turret.draw(screen)
            enemy_group.draw(screen)
        
            draw_text(str(game_map.hp), text_font, "black", game_map.width*cs.TILE_SIZE+10, 0, screen)
            draw_text(str(game_map.money), text_font, "black", game_map.width*cs.TILE_SIZE+100, 0, screen)
            buy_turret_button.draw(screen)
        else:
            draw_text("You lost" if game_outcome == -1 else "You won", text_font, "black", 500, 200, screen)
        
        if not game_over:
            if placing_turrets:  
                turret1_button.draw(screen)
                turret2_button.draw(screen)
                turret3_button.draw(screen)
                cancel_button.draw(screen)

            if selected_turret and not placing_turrets and selected_turret.upgrade_turret < cs.TURRET_MAX_LEVEL:
                upgrade_button.draw(screen)
            
            if not level_started:
                start_wave_button.draw(screen)
            else:
                if pg.time.get_ticks() - last_enemy_spawn > cs.SPAWN_RATE:
                    if game_map.spawned_enemy < len(game_map.enemy_list):
                        enemy_type = game_map.enemy_list[game_map.spawned_enemy]
                        enemy = Enemy(game_map, enemy_type)
                        enemy_group.add(enemy)
                        game_map.spawned_enemy += 1
                        last_enemy_spawn = pg.time.get_ticks()
            
            if game_map.level_finished():
                level_started = False
                if game_map.level==1:
                    map_loaded = game_map.load_from_file('maps/level2.txt')
                    for turret in turret_group:
                        turret.delete_turret()
                    game_map.level += 1
                    show_popup(screen, "To jest popup!")
                elif game_map.level==2:
                    map_loaded = game_map.load_from_file('maps/level3.txt')
                    for turret in turret_group:
                        turret.delete_turret()
                    game_map.level += 1
                    show_popup(screen, "To jest popup!")
                elif game_map.level == 3:
                    game_over = True
                    game_outcome = 1
                else:
                    ENEMY_SPAWN_DATA[3]["normal"]+=1
                    ENEMY_SPAWN_DATA[3]["heavy"]+=1
                    ENEMY_SPAWN_DATA[3]["fast"]+=1
                last_enemy_spawn = pg.time.get_ticks()
                game_map.reset_level()
                game_map.process_enemies()
                game_map.money += cs.LEVEL_COMPLETE_REWARD
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            
            if buy_turret_button.is_clicked(event):
                placing_turrets = True
            
            if start_wave_button.is_clicked(event):
                level_started = True
                
            if placing_turrets:
                if turret1_button.is_clicked(event):
                    selected_turret_type = "tower_1"
                    update_turret_button_colors()
                elif turret2_button.is_clicked(event):
                    selected_turret_type = "tower_2"
                    update_turret_button_colors()
                elif turret3_button.is_clicked(event):
                    selected_turret_type = "tower_3"
                    update_turret_button_colors()
            
            if cancel_button.is_clicked(event):
                placing_turrets = False
            
            if upgrade_button.is_clicked(event) and selected_turret and selected_turret.upgrade_turret < cs.TURRET_MAX_LEVEL and not placing_turrets and game_map.money >= cs.UPGRADE_COST:
                selected_turret.upgrade()
            
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pg.mouse.get_pos()
                # Check if click is within map boundaries
                if mouse_pos[0] < game_map.width * cs.TILE_SIZE and mouse_pos[1] < game_map.height * cs.TILE_SIZE:
                    # First check if we clicked on a turret
                    turret_clicked = False
                    for turret in turret_group:
                        if turret.rect.collidepoint(mouse_pos):
                            # Select this turret
                            for t in turret_group:
                                t.selected = False  # Deselect all other turrets
                            turret.selected = True
                            selected_turret = turret
                            turret_clicked = True
                            break
                    
                    # If we didn't click on a turret, handle other cases
                    if not turret_clicked:
                        # Deselect all turrets when clicking elsewhere
                        for turret in turret_group:
                            turret.selected = False
                        selected_turret = None
                        
                        # Handle turret placement if we're in placement mode
                        if placing_turrets:
                            # Get the tile at the clicked position
                            clicked_tile = game_map.get_tile_at_position(mouse_pos[0], mouse_pos[1])
                    
                            # Check if tile is valid for turret placement (grass tiles only)
                            if clicked_tile and clicked_tile.tile_type == 'grass':
                                # Check if there's already a turret on this tile
                                tile_center = (clicked_tile.rect.centerx, clicked_tile.rect.centery)
                                
                                # Check for existing turrets at this position
                                turret_exists = False
                                for turret in turret_group:
                                    if turret.tile_pos == (clicked_tile.rect.x // cs.TILE_SIZE, clicked_tile.rect.y // cs.TILE_SIZE):
                                        turret_exists = True
                                        break
                                
                                # Place turret if none exists at this position
                                if not turret_exists and game_map.money >= cs.BUY_COST:
                                    turret = Turret(tile_center, selected_turret_type, tile_pos=(clicked_tile.rect.x // cs.TILE_SIZE, clicked_tile.rect.y // cs.TILE_SIZE))
                                    turret_group.add(turret)
                                    game_map.money -= cs.BUY_COST
        
        pg.display.flip()
    
    pg.quit()

# Main program entry point
if __name__ == "__main__":
    # Show mode selection menu
    game_mode = show_mode_selection_menu()
    
    # Only start the game if a mode was selected
    if game_mode is not None:
        main(game_mode)
    else:
        pg.quit()