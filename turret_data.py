# Turret stats configuration
# Each key represents a turret type or its upgraded version.
# Values are dictionaries defining:
# - range: radius of attack area (in pixels)
# - attack_speed: time between shots (in milliseconds)
# - damage: how much HP is subtracted per hit

TURRET_DATA = {
    "tower_1": {
        "range": 100,         # Basic tower: small range
        "attack_speed": 500,  # Shoots every 0.5s
        "damage": 1           # Deals 1 damage per shot
    },
    "tower_1_upgrade": {
        "range": 150,         # Increased range
        "attack_speed": 250,  # Faster firing (every 0.25s)
        "damage": 2           # Deals more damage
    },
    "tower_2": {
        "range": 150,         # Good range
        "attack_speed": 1500, # Slower firing (1.5s between shots)
        "damage": 2           # Moderate damage
    },
    "tower_2_upgrade": {
        "range": 200,         # Large range
        "attack_speed": 1000, # Faster than base version
        "damage": 4           # Strong hit
    },
    "tower_3": {
        "range": 125,         # Medium range
        "attack_speed": 1000, # Fires every second
        "damage": 2           # Balanced damage
    },
    "tower_3_upgrade": {
        "range": 150,
        "attack_speed": 500,  # Faster fire rate
        "damage": 3           # Increased damage
    }
}
