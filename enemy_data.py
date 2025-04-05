# Enemy spawn configuration for each level.
# Each dictionary in the list represents one level.
# Keys represent enemy types, values represent how many of each to spawn.
ENEMY_SPAWN_DATA = [
    {
        "normal": 10,  # Level 1: 10 normal enemies
        "heavy": 0,
        "fast": 0,
        "boss": 0,
    },
    {
        "normal": 10,  # Level 2: 10 normal, 5 heavy, 2 fast enemies
        "heavy": 5,
        "fast": 2,
        "boss": 0,
    },
    {
        "normal": 5,   # Level 3: 5 normal, 3 heavy, 1 boss enemy
        "heavy": 3,
        "fast": 0,
        "boss": 1,
    },
    {
        "normal": 10,  # Endless wave template (used repeatedly)
        "heavy": 0,
        "fast": 0,
    }
]

# Stats for each enemy type
# Defines their health points (hp) and movement speed
ENEMY_DATA = {
    "normal": {
        "hp": 10,      # Standard enemy with balanced stats
        "speed": 2
    },
    "heavy": {
        "hp": 20,      # Tougher version 
        "speed": 2     
    },
    "fast": {
        "hp": 3,       # Weaker but much faster enemy
        "speed": 4
    },
    "boss": {
        "hp": 50,      # High-HP boss unit, usually one per level
        "speed": 2
    }
}
