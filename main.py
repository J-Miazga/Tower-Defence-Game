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
from config_dialog import get_config, select_save_source
from save_and_load import json_manager,xml_manager,mongodb_manager


def show_start_menu():
    # Create and configure the Pygame window for the start menu
    screen = pg.display.set_mode((400, 300))
    pg.display.set_caption("Start Menu")
    font = pg.font.SysFont("Consolas", 32)
    clock = pg.time.Clock()

    # Define buttons for "Start New Game" and "Continue"
    start_button = pg.Rect(100, 100, 200, 50)
    continue_button = pg.Rect(100, 180, 200, 50)

    while True:
        screen.fill("lightgray")

        # Draw the buttons
        pg.draw.rect(screen, "green", start_button, border_radius=8)
        pg.draw.rect(screen, "dodgerblue", continue_button, border_radius=8)

        # Render button labels
        start_text = font.render("Start New Game", True, "white")
        continue_text = font.render("Continue", True, "white")

        # Blit text centered in each button
        screen.blit(start_text, start_text.get_rect(center=start_button.center))
        screen.blit(continue_text, continue_text.get_rect(center=continue_button.center))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                # If "Start New Game" clicked, return the action
                if start_button.collidepoint(event.pos):
                    return "new"
                # If "Continue" clicked, open file format selection and load accordingly
                elif continue_button.collidepoint(event.pos):
                    save_source = select_save_source()  # Prompt user to choose save format

                    if save_source == "json":
                        save_data = json_manager.load()
                    elif save_source == "xml":
                        save_data = xml_manager.load()
                    elif save_source == "mongo":
                        save_data = mongodb_manager.load()

                    # If data is loaded successfully, return it with "continue"
                    if save_data:
                        return "continue", save_data
                    else:
                        print("No save file found.")
                        return "new"  # fallback to new game if no save found

        pg.display.flip()
        clock.tick(30)  # Limit to 30 FPS


def load_game_progress(game_map, save_data):
    # Restore saved game state into the map object
    game_map.level = save_data.get("level", 1)          # Set the saved level (default 1)
    game_map.hp = save_data.get("hp", cs.HEALTH)        # Restore health or use default
    game_map.money = save_data.get("money", cs.MONEY)   # Restore money or use default

    turrets_to_restore = save_data.get("turrets", [])   # Retrieve list of turrets to restore

    # If it's endless mode (level 4), load wave and enemy data
    if game_map.level == 4:
        wave = save_data.get("wave", 0)
        enemy_wave = save_data.get("enemy_data", {})
        LEVEL_DATA[4]["wave"] = wave                    # Restore current wave count
        ENEMY_SPAWN_DATA[3].update(enemy_wave)          # Update enemy counts for spawning

    # Determine which map file to load based on level
    map_file = "maps/endless_level.txt" if game_map.level == 4 else f"maps/level{game_map.level}.txt"
    map_loaded = game_map.load_from_file(map_file)      # Load the corresponding map

    return turrets_to_restore, map_loaded               # Return turret data and map loading status



def collect_save_data_json(game_map, turret_group):
    # Prepare a dictionary containing all necessary game state data for saving
    return {
        "level": game_map.level,             # Current level of the game
        "hp": game_map.hp,                   # Player's current health
        "money": game_map.money,             # Current in-game currency

        # Save data for all turrets on the map
        "turrets": [
            {
                "x": t.rect.centerx,         # X coordinate of the turret
                "y": t.rect.centery,         # Y coordinate of the turret
                "type": t.tower_type,        # Type of turret (e.g., tower_1)
                "level": t.upgrade_turret    # Upgrade level of the turret
            } for t in turret_group
        ],

        "wave": LEVEL_DATA.get(4, {}).get("wave", 0),   # Current wave number (for endless mode)
        "enemy_data": ENEMY_SPAWN_DATA[3]               # Number of enemies per type for endless mode
    }


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

def restore_turrets_from_data(turrets_data, turret_group):
    from turrets import Turret  # Import the Turret class

    # Recreate turret instances based on saved data
    for turret_info in turrets_data:
        turret = Turret(
            (turret_info["x"], turret_info["y"]),  # Set position
            turret_info["type"]                    # Set turret type
        )
        turret.upgrade_turret = turret_info["level"]  # Restore upgrade level
        turret_group.add(turret)  # Add turret to the turret group



def show_mode_selection_menu():
    # Create a small window for the game mode selection menu
    menu_screen = pg.display.set_mode((400, 400))
    pg.display.set_caption("Game Mode Selection")

    # Define fonts for title and buttons
    title_font = pg.font.SysFont("Consolas", 36, bold=True)
    button_font = pg.font.SysFont("Consolas", 24)

    # Create buttons for Endless and Story (Plot) modes
    endless_button = Button(100, 150, 200, 50, "Endless Mode", button_font)
    plot_button = Button(100, 220, 200, 50, "Story Mode", button_font)

    # Menu event loop
    while True:
        menu_screen.fill("grey100")  # Fill background color
        draw_text("Select Game Mode", title_font, "black", 50, 50, menu_screen)

        # Draw mode selection buttons
        endless_button.draw(menu_screen)
        plot_button.draw(menu_screen)

        # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                # Exit the game if the user closes the window
                pg.quit()
                return None, None

            # Return selected game mode
            if endless_button.is_clicked(event):
                return 'endless', None

            if plot_button.is_clicked(event):
                return 'plot', None

        # Update display
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

    if level_info and game_map.level != 4:
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
    elif game_map.level == 4:
        # Endless mode logic
        wave = LEVEL_DATA[4].get("wave", 0) + 1
        LEVEL_DATA[4]["wave"] = wave
        ENEMY_SPAWN_DATA[3]["normal"] += 1
        ENEMY_SPAWN_DATA[3]["heavy"] += 1
        ENEMY_SPAWN_DATA[3]["fast"] += 1

    game_map.generate_enemy_list()
    # Saves to different formats
    json_manager.save(collect_save_data_json(game_map,turret_group))
    xml_manager.save(collect_save_data_json(game_map,turret_group))
    mongodb_manager.save(collect_save_data_json(game_map,turret_group))

    return False, 0

# === MAIN GAME LOOP ===
def main(game_mode, game_map, mission,save_data=None):
    clock = pg.time.Clock()
    last_enemy_spawn = pg.time.get_ticks()
    
    if game_mode == 'endless':
        map_loaded = game_map.load_from_file('maps/endless_level.txt')
        game_map.level = 4
        plot = None

    elif game_mode == 'continue' and save_data:
        plot = None
        turrets_to_restore, map_loaded = load_game_progress(game_map, save_data)

    else:  # story mode
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
    # Add turrets from previous save
    if game_mode == 'continue' and save_data:
        restore_turrets_from_data(turrets_to_restore, turret_group)



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
    # Initialize Pygame and set the default font
    pg.init()
    font = pg.font.SysFont(None, 36)
   
    # Show initial menu: "Start New Game" or "Continue"
    choice = show_start_menu()

    # If user selected "Continue", extract saved game mode and data
    if isinstance(choice, tuple) and choice[0] == "continue":
        game_mode = "continue"
        save_data = choice[1]
    else:
        # Otherwise, get game configuration via Tkinter dialog
        config = get_config()
        if config:
            # Save configuration to all supported formats (JSON, XML, MongoDB)
            json_manager.save({"config": config})
            mongodb_manager.save({"config": config})
            xml_manager.save({"config": config})

            # Let user choose game mode (Endless or Plot)
            game_mode, save_data = show_mode_selection_menu()
        else:
            # Exit if config dialog was cancelled
            pg.quit()
            exit()

    # Initialize core game components
    game_map = Map()
    mission = MissionManager()

    # Launch the main game loop with chosen mode and saved data (if any)
    main(game_mode, game_map, mission, save_data)

    
