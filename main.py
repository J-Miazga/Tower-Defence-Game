import pygame as pg
import constant as cs
from enemies import Enemy
from map import Map
from turrets import Turret
from buttons import Button
from enemy_data import ENEMY_SPAWN_DATA
from level_data import LEVEL_DATA
from story_and_missions import StoryManager, MissionManager
from logger import game_logger

# Draws text onto the screen at a specified position
def draw_text(text, font, text_col, x, y, surface):
    img = font.render(text, True, text_col)
    surface.blit(img, (x, y))

# Checks whether the game is over based on the player's HP
def check_game_over(game_map):
    return game_map.hp <= 0

# Updates all game entities like enemies and turrets
def update_game_state(enemy_group, turret_group):
    enemy_group.update()
    for turret in turret_group:
        turret.update(enemy_group)

# Loads a specific level from file
def load_level(level):
    filename = f"maps/level{level}.txt"
    success = game_map.load_from_file(filename)
    if success:
        game_map.reset_level()
        game_map.generate_enemy_list()
        game_map.level = level
        return True
    else:
        game_logger.log(f"Failed to load map for level {level}", "error")
        return False

# Displays the initial menu to choose game mode (endless or plot)
def show_mode_selection_menu():
    menu_screen = pg.display.set_mode((400, 300))
    pg.display.set_caption("Game Mode Selection")
    title_font = pg.font.SysFont("Consolas", 36, bold=True)
    button_font = pg.font.SysFont("Consolas", 24)

    endless_button = Button(100, 150, 200, 50, "Endless Wave", button_font)
    plot_button = Button(100, 220, 200, 50, "Plot Mode", button_font)

    while True:
        menu_screen.fill("grey100")
        draw_text("Select Game Mode", title_font, "black", 50, 50, menu_screen)
        endless_button.draw(menu_screen)
        plot_button.draw(menu_screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return None
            if endless_button.is_clicked(event):
                return 'endless'
            if plot_button.is_clicked(event):
                return 'plot'

        pg.display.flip()

# Handles drawing of all main game elements including turrets, enemies, and UI buttons
def draw_game_elements(screen, game_map, turret_group, enemy_group, mission, font,
                       placing_turrets, cursor_x, cursor_y, selected_turret,
                       upgrade_button, buy_turret_button, cancel_button,
                       start_wave_button, level_started,
                       turret1_button, turret2_button, turret3_button):

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
    game_logger.display.draw(screen, font, 10, game_map.height * cs.TILE_SIZE - 250, game_map.width * cs.TILE_SIZE)
    if not mission.check_upgrade_mission(turret_group, game_map):
        mission.draw_mission(screen, font)

    draw_text(f"HP: {game_map.hp}", font, "black", game_map.width * cs.TILE_SIZE + 10, 0, screen)
    draw_text(f"Money: {game_map.money}", font, "black", game_map.width * cs.TILE_SIZE + 100, 0, screen)
    buy_turret_button.draw(screen)

    if placing_turrets:
        turret1_button.draw(screen)
        turret2_button.draw(screen)
        turret3_button.draw(screen)
        cancel_button.draw(screen)

    if selected_turret and not placing_turrets and selected_turret.upgrade_turret < cs.TURRET_MAX_LEVEL:
        upgrade_button.draw(screen)

    if not level_started:
        start_wave_button.draw(screen)

# Handles spawning of enemies based on a spawn timer
def handle_wave_spawning(game_map, enemy_group, last_enemy_spawn):
    current_time = pg.time.get_ticks()
    if current_time - last_enemy_spawn > cs.SPAWN_RATE:
        if game_map.spawned_enemy < len(game_map.enemy_list):
            enemy_type = game_map.enemy_list[game_map.spawned_enemy]
            enemy = Enemy(game_map, enemy_type)
            enemy_group.add(enemy)
            game_map.spawned_enemy += 1
            return current_time
    return last_enemy_spawn

# Handles what happens when a level is completed (story mode or endless)
def handle_level_progression(game_map, turret_group, mission, plot):
    game_map.reset_level()
    game_map.money += cs.LEVEL_COMPLETE_REWARD
    level_info = LEVEL_DATA.get(game_map.level)

    if level_info:
        if level_info.get("reset_turrets"):
            for turret in turret_group:
                turret.delete_turret()

        if mission_text := level_info.get("set_mission"):
            mission.set_mission(mission_text)

        if level_info.get("end_game"):
            plot.show_popup(level_info["story"])
            return True, 1
        else:
            game_map.load_from_file(level_info["map"])
            game_map.level += 1
            plot.show_popup(level_info["story"])
    else:
        # Endless mode logic
        ENEMY_SPAWN_DATA[3]["normal"] += 1
        ENEMY_SPAWN_DATA[3]["heavy"] += 1
        ENEMY_SPAWN_DATA[3]["fast"] += 1

    game_map.generate_enemy_list()
    return False, 0

# === MAIN GAME LOOP ===
def main(game_mode, game_map, mission):
    clock = pg.time.Clock()
    last_enemy_spawn = pg.time.get_ticks()

    # Load starting map
    if game_mode == 'endless':
        map_loaded = game_map.load_from_file('maps/endless_level.txt')
        game_map.level = 4
        plot = None
    else:
        map_loaded = game_map.load_from_file('maps/level1.txt')

    if not map_loaded:
        game_logger.log("Failed to load map!", "error")
        return

    # Set up screen and story (if applicable)
    screen = pg.display.set_mode((game_map.width * cs.TILE_SIZE + cs.SIDE_PANEL, game_map.height * cs.TILE_SIZE))
    pg.display.set_caption("Tower Defense Game")

    if game_mode == "plot":
        plot = StoryManager(screen, font)
        plot.show_popup("Dowództwo do wszystkich jednostek! Wróg przekroczył granicę i przemieszcza się w kierunku naszej bazy. Rozstawcie wieżyczki i powstrzymajcie ich za wszelką cenę. Jeśli padniemy tutaj, reszta kraju nie ma szans.")
        mission.set_mission("Upgrade Tower")

    game_map.generate_enemy_list()
    enemy_group = pg.sprite.Group()
    turret_group = pg.sprite.Group()

    # UI buttons
    upgrade_button = Button(game_map.width * cs.TILE_SIZE + 75, 60, 200, 50, "Upgrade turret", font)
    buy_turret_button = Button(game_map.width * cs.TILE_SIZE + 75, 120, 150, 50, "Buy turret", font)
    cancel_button = Button(game_map.width * cs.TILE_SIZE + 75, 300, 150, 50, "Cancel", font)
    start_wave_button = Button(game_map.width * cs.TILE_SIZE + 75, 400, 150, 50, "Start wave", font)

    turret1_button = Button(game_map.width * cs.TILE_SIZE + 25, 180, 100, 40, "Tower 1", font)
    turret2_button = Button(game_map.width * cs.TILE_SIZE + 135, 180, 100, 40, "Tower 2", font)
    turret3_button = Button(game_map.width * cs.TILE_SIZE + 75, 230, 100, 40, "Tower 3", font)

    # Game state flags
    placing_turrets = False
    selected_turret = None
    selected_turret_type = "tower_1"
    dragging_turret = False
    dragged_turret_image = None
    level_started = False
    game_over = False
    game_outcome = 0
    cursor_x, cursor_y = 0, 0

    # Main game loop
    run = True
    while run:
        clock.tick(cs.FPS)
        screen.fill("grey100")

        # === GAME LOGIC ===
        if not game_over:
            if check_game_over(game_map):
                game_over = True
                game_outcome = -1

            update_game_state(enemy_group, turret_group)

            draw_game_elements(screen, game_map, turret_group, enemy_group, mission, font,
                               placing_turrets, cursor_x, cursor_y, selected_turret,
                               upgrade_button, buy_turret_button, cancel_button,
                               start_wave_button, level_started,
                               turret1_button, turret2_button, turret3_button)

            if level_started:
                last_enemy_spawn = handle_wave_spawning(game_map, enemy_group, last_enemy_spawn)

            if game_map.level_finished():
                level_started = False
                game_over, game_outcome = handle_level_progression(game_map, turret_group, mission, plot)

        else:
            draw_text("You lost" if game_outcome == -1 else "You won", font, "black", 500, 200, screen)


        for event in pg.event.get():

            # === SYSTEM ===
            if event.type == pg.QUIT:
                run = False

            # === MOUSE CLICK HANDLING ===
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:

                # UI Buttons
                if buy_turret_button.is_clicked(event):
                    placing_turrets = True
                elif start_wave_button.is_clicked(event):
                    level_started = True
                elif cancel_button.is_clicked(event):
                    placing_turrets = False
                elif upgrade_button.is_clicked(event) and selected_turret and not placing_turrets:
                    if selected_turret.upgrade_turret < cs.TURRET_MAX_LEVEL and game_map.money >= cs.UPGRADE_COST:
                        selected_turret.upgrade()
                        game_logger.log(f"Upgraded turret at {selected_turret.tile_pos} to level {selected_turret.upgrade_turret}", "info")
                        game_map.money -= cs.UPGRADE_COST

                # Choose turret type (during placing)
                if placing_turrets:
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

                # Select existing turret
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

            # === MOUSE BUTTON RELEASE (for placing) ===
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1 and dragging_turret:
                mouse_pos = pg.mouse.get_pos()
                if mouse_pos[0] < game_map.width * cs.TILE_SIZE and mouse_pos[1] < game_map.height * cs.TILE_SIZE:
                    tile = game_map.get_tile_at_position(mouse_pos[0], mouse_pos[1])
                    if tile:
                        tile_center = tile.rect.center
                        tile_pos = (tile.rect.x // cs.TILE_SIZE, tile.rect.y // cs.TILE_SIZE)
                        if tile.tile_type == 'grass' and not any(t.tile_pos == tile_pos for t in turret_group) and game_map.money >= cs.BUY_COST:
                            turret = Turret(tile_center, selected_turret_type, tile_pos)
                            turret_group.add(turret)
                            game_logger.log(f"Placed {selected_turret_type} at {tile_pos}", "info")
                            game_map.money -= cs.BUY_COST
                        else:
                            game_logger.log(f"Invalid turret placement attempt at {tile_pos}", "warning")
                dragging_turret = False
                dragged_turret_image = None

            # === KEYBOARD INPUT ===
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKQUOTE:  # toggle log
                    game_logger.display.toggle()

                # Keyboard turret placement
                elif event.key == pg.K_1:
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

                # Move keyboard cursor
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
                            game_logger.log(f"Placed {selected_turret_type} at {tile_pos}", "info")
                            game_map.money -= cs.BUY_COST
                        else:
                            game_logger.log(f"Invalid turret placement attempt at {tile_pos}", "warning")

        # === Draw dragged turret image ===
        if dragging_turret and dragged_turret_image:
            mouse_x, mouse_y = pg.mouse.get_pos()
            img_rect = dragged_turret_image.get_rect(center=(mouse_x, mouse_y))
            screen.blit(dragged_turret_image, img_rect)

        pg.display.flip()

    pg.quit()
# === ENTRY POINT ===
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
