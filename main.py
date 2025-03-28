import pygame as pg
import constant as cs
from enemies import Enemy
from map import Map
from tiles import Tile
from turrets import Turret
from buttons import Button
from enemy_data import ENEMY_SPAWN_DATA
from story_and_missions import StoryScene,MissionManager
from logger import game_logger

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
        draw_text("Select Game Mode", title_font, "black", 50, 50, menu_screen)
        
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

def main(game_mode,game_map,mission):
    clock = pg.time.Clock()
    last_enemy_spawn = pg.time.get_ticks()

    #game_map = Map()
    if game_mode == 'endless':
        map_loaded = game_map.load_from_file('maps/endless_level.txt')
        game_map.level=4
    else:
        map_loaded = game_map.load_from_file('maps/level1.txt')

    if not map_loaded:
        game_logger.log("Failed to load map!","error")
        return

    screen = pg.display.set_mode((game_map.width*cs.TILE_SIZE+cs.SIDE_PANEL, game_map.height*cs.TILE_SIZE))
    pg.display.set_caption("Tower Defense Game")
    plot=StoryScene(screen,font)
    plot.draw("Dowództwo do wszystkich jednostek! Wróg przekroczył granicę i przemieszcza się w kierunku naszej bazy. Rozstawcie wieżyczki i powstrzymajcie ich za wszelką cenę. Jeśli padniemy tutaj, reszta kraju nie ma szans.")

    game_map.process_enemies()
    text_font = pg.font.SysFont("Consolas", 24, bold=True)
    enemy_group = pg.sprite.Group()
    turret_group = pg.sprite.Group()
  

    DEFAULT_BUTTON_COLOR = (50, 150, 50)
    SELECTED_BUTTON_COLOR = (100, 100, 255)

    upgrade_button = Button(game_map.width*cs.TILE_SIZE+75, 60, 150, 50, "Upgrade turret", font)
    buy_turret_button = Button(game_map.width*cs.TILE_SIZE+75, 120, 150, 50, "Buy turret", font)
    cancel_button = Button(game_map.width*cs.TILE_SIZE+75, 300, 150, 50, "Cancel", font)
    start_wave_button = Button(game_map.width*cs.TILE_SIZE+75, 400, 150, 50, "Start wave", font)

    turret1_button = Button(game_map.width*cs.TILE_SIZE+25, 180, 100, 40, "Tower 1", font)
    turret2_button = Button(game_map.width*cs.TILE_SIZE+135, 180, 100, 40, "Tower 2", font)
    turret3_button = Button(game_map.width*cs.TILE_SIZE+75, 230, 100, 40, "Tower 3", font)

    placing_turrets = False
    selected_turret = None
    selected_turret_type = "tower_1"
    dragging_turret = False
    dragged_turret_image = None
    level_started = False
    game_over = False
    game_outcome = 0

    cursor_x, cursor_y = 0, 0

    mission.set_mission("Upgrade Tower")
    

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

            if placing_turrets:
                if 0 <= cursor_x < game_map.width and 0 <= cursor_y < game_map.height:
                    tile = game_map.tiles[cursor_y][cursor_x]
                    highlight = pg.Surface((cs.TILE_SIZE, cs.TILE_SIZE))
                    highlight.fill((0, 0, 0))
                    highlight.set_alpha(100)
                    screen.blit(highlight, tile.rect.topleft)

            for turret in turret_group:
                turret.draw(screen)
            enemy_group.draw(screen)

            if not mission.check_turret_upgrade_mission(turret_group):
                mission.render_mission(screen,font)
            else:
                game_map.money += 300

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
                    mission.set_mission("Upgrade Tower")
                    for turret in turret_group:
                        turret.delete_turret()
                    game_map.level += 1
                    plot.draw("Zwiad meldował większe siły niż przewidywaliśmy. Wróg zaczyna używać ciężkiego sprzętu. Nasze wieżyczki z minigunami dają radę, ale to już nie są zwykłe potyczki. To wojna na pełną skalę.")
                elif game_map.level==2:
                    map_loaded = game_map.load_from_file('maps/level3.txt')
                    mission.set_mission("Upgrade Tower")
                    for turret in turret_group:
                        turret.delete_turret()
                    game_map.level += 1
                    plot.draw("To już ostatnia linia obrony. Jeśli ją stracimy, wszystko przepada. Zyskaliśmy trochę czasu dzięki rakietowym wieżyczkom, ale wróg rzuca wszystko, co ma. Przygotujcie się – nie będzie odwrotu.")
                elif game_map.level == 3:
                    mission.set_mission("Upgrade Tower")
                    game_over = True
                    game_outcome = 1
                    plot.draw("Udało się. Obroniliśmy bazę, a wróg się wycofuje. Straty są duże, ale pokazaliśmy, że nie damy się złamać. Teraz my przechodzimy do ataku.")
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

            if cancel_button.is_clicked(event):
                placing_turrets = False

            if upgrade_button.is_clicked(event) and selected_turret and selected_turret.upgrade_turret < cs.TURRET_MAX_LEVEL and not placing_turrets and game_map.money >= cs.UPGRADE_COST:
                selected_turret.upgrade()
                game_logger.log(f"Upgraded turret at {selected_turret.tile_pos} to level {selected_turret.upgrade_turret}","info")
                game_map.money -= cs.UPGRADE_COST
            
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and placing_turrets:
                if turret1_button.rect.collidepoint(event.pos):
                    selected_turret_type = "tower_1"
                    dragging_turret = True
                    dragged_turret_image = Turret((0, 0), selected_turret_type).image
                elif turret2_button.rect.collidepoint(event.pos):
                    selected_turret_type = "tower_2"
                    dragging_turret = True
                    dragged_turret_image = Turret((0, 0), selected_turret_type).image
                elif turret3_button.rect.collidepoint(event.pos):
                    selected_turret_type = "tower_3"
                    dragging_turret = True
                    dragged_turret_image = Turret((0, 0), selected_turret_type).image

            if event.type == pg.KEYDOWN:
                
                if event.key == pg.K_BACKQUOTE:  # ` key
                    game_logger.display.toggle()
                if event.key == pg.K_1:
                    selected_turret_type = "tower_1"
                    placing_turrets = True
                elif event.key == pg.K_2:
                    selected_turret_type = "tower_2"
                    placing_turrets = True
                elif event.key == pg.K_3:
                    selected_turret_type = "tower_3"
                    placing_turrets = True
                elif event.key == pg.K_ESCAPE:
                    placing_turrets = False

                if placing_turrets:
                    if event.key == pg.K_w and cursor_y > 0:
                        cursor_y -= 1
                    elif event.key == pg.K_s and cursor_y < game_map.height - 1:
                        cursor_y += 1
                    elif event.key == pg.K_a and cursor_x > 0:
                        cursor_x -= 1
                    elif event.key == pg.K_d and cursor_x < game_map.width - 1:
                        cursor_x += 1
                    elif event.key == pg.K_RETURN:
                        tile = game_map.tiles[cursor_y][cursor_x]
                        tile_pos = (cursor_x, cursor_y)
                        tile_center = tile.rect.center
                        if tile.tile_type == 'grass' and not any(t.tile_pos == tile_pos for t in turret_group) and game_map.money >= cs.BUY_COST:
                            turret = Turret(tile_center, selected_turret_type, tile_pos)
                            turret_group.add(turret)
                            game_logger.log(f"Placed {selected_turret_type} at {tile_pos}","info")
                            game_map.money -= cs.BUY_COST
                        else:
                            game_logger.log(f"Invalid turret placement attempt at {tile_pos}","warning")

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pg.mouse.get_pos()
                if mouse_pos[0] < game_map.width * cs.TILE_SIZE and mouse_pos[1] < game_map.height * cs.TILE_SIZE:
                    turret_clicked = False
                    for turret in turret_group:
                        if turret.rect.collidepoint(mouse_pos):
                            for t in turret_group:
                                t.selected = False
                            turret.selected = True
                            selected_turret = turret
                            turret_clicked = True
                            break
                    if not turret_clicked:
                        for turret in turret_group:
                            turret.selected = False
                        selected_turret = None

            elif event.type == pg.MOUSEBUTTONUP and event.button == 1 and dragging_turret:
                mouse_pos = pg.mouse.get_pos()
                tile = game_map.get_tile_at_position(mouse_pos[0], mouse_pos[1])
                tile_center = tile.rect.center
                tile_pos = (tile.rect.x // cs.TILE_SIZE, tile.rect.y // cs.TILE_SIZE)
                if tile.tile_type == 'grass' and not any(t.tile_pos == tile_pos for t in turret_group) and game_map.money >= cs.BUY_COST:
                    turret = Turret(tile_center, selected_turret_type, tile_pos)
                    turret_group.add(turret)
                    game_logger.log(f"Placed {selected_turret_type} at {tile_pos}","info")
                    game_map.money -= cs.BUY_COST
                else:
                    game_logger.log(f"Invalid turret placement attempt at {tile_pos}","warning")
                dragging_turret = False
                dragged_turret_image = None

        if dragging_turret and dragged_turret_image:
            mouse_x, mouse_y = pg.mouse.get_pos()
            img_rect = dragged_turret_image.get_rect(center=(mouse_x, mouse_y))
            screen.blit(dragged_turret_image, img_rect)
        
        game_logger.display.draw(screen, font, 10, game_map.height * cs.TILE_SIZE - 250,game_map.width*cs.TILE_SIZE)
        pg.display.flip()

    pg.quit()

if __name__ == "__main__":
    pg.init()
    font = pg.font.SysFont(None, 36)
    game_mode = show_mode_selection_menu()
    game_map = Map()
    mission=MissionManager()
    if game_mode is not None:
        main(game_mode,game_map,mission)
    else:
        pg.quit()