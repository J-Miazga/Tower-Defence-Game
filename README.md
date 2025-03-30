# Tower Defense Game (Python + Pygame)

This is a **Tower Defense game** written in Python using the **Pygame** library. It was developed as part of lab exercises for a university course.

## About the Project
In this game, the player defends their base by strategically placing and upgrading turrets on a map. Waves of enemies follow a path to reach the base. The player loses health when enemies get through and earns money by defeating them. The game includes both an **Endless Mode** and a **Plot Mode** with story-based progression and objectives.

## Features
- **Turret System**: Multiple turret types with upgrade levels.
- **Enemy Types**: Normal, Heavy, Fast, and Boss enemies with distinct stats.
- **Map System**: Tile-based maps with different terrain types affecting movement.
- **Pathfinding**: Enemies use A* algorithm to navigate to the base.
- **Story Progression**: In Plot Mode, players receive mission pop-ups and objectives.
- **Logger**: Game actions are logged and can be toggled on/off in-game.
- **Keyboard + Mouse Controls**: Supports both cursor and key-based turret placement.

---

## Class Descriptions

### `main.py`
- **Main loop** and core game logic: handling updates, rendering, input, and level progression.

### `Map`
- Loads maps from files.
- Manages tile grid, enemy spawns, and level state.

### `Tile`
- Represents individual tiles (e.g. path, grass, mountain).
- Contains movement cost for pathfinding.

### `Enemy`
- Handles movement, pathfinding (A*), health, and death.
- Uses `ENEMY_DATA` to load enemies properties.

### `Turret`
- Manages targeting, rotation, firing, upgrades, and visuals.
- Uses `TURRET_DATA` to load turret properties.

### `Button`
- GUI button class for the main menu and in-game UI.

### `StoryManager`
- Shows plot popups with mission briefings.

### `MissionManager`
- Tracks player objectives (e.g. upgrade a turret) and gives rewards.

### `GameLogger`
- Logs key events to file and optionally displays them in-game.

---

## How to Run
### Requirements
- Python 3.8+
- Pygame (`pip install pygame`)

### Run the Game
```bash
python main.py
```

### Controls
- **Mouse**: UI interactions and turret placement
- **W/A/S/D**: Move tile selector when using keyboard placement
- **1/2/3**: Select turret type
- **Enter**: Place turret at selected tile
- **Escape**: Cancel placement
- **Backquote (\`)**: Toggle log window

---

## Folders Structure
```
project/
|-- main.py
|-- constant.py
|-- turrets.py
|-- enemies.py
|-- map.py
|-- tiles.py
|-- buttons.py
|-- pathfinding.py
|-- story_and_missions.py
|-- logger.py
|-- enemy_data.py
|-- turret_data.py
|-- level_data.py
|-- maps/
|   |-- level1.txt
|   |-- level2.txt
|   |-- level3.txt
|   |-- endless_level.txt
|-- Sprites/
    |-- towers/
    |-- enemies/
    |-- tiles/
```

---

## Author & Notes
Created as a lab assignment project. The codebase is modular and designed for easy extension (new levels, turrets, enemies, etc.).


