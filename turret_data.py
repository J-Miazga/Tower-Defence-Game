TURRET_DATA = [
    {
        "range":100,
        "attack_speed":500,
        "damage":1
    },
    {
        "range":150,
        "attack_speed":250,
        "damage":2
    },
    {
        "range":150,
        "attack_speed":1500,
        "damage":2
    },
    {
        "range":200,
        "attack_speed":1000,
        "damage":4
    },
    {
        "range":125,
        "attack_speed":1000,
        "damage":2
    },
    {
        "range":150,
        "attack_speed":500,
        "damage":3
    }
]

# def get_turret_data(turret_type, level):
#     if turret_type == "tower_1":
#         base_index = 0
#     elif turret_type == "tower_2":
#         base_index = 2
#     elif turret_type == "tower_3":
#         base_index = 4
#     else:
#         base_index = 0
    
#     # Calculate the index based on level
#     index = base_index + (level - 1)
    
#     # Make sure we don't go out of bounds
#     if index >= len(TURRET_DATA):
#         index = len(TURRET_DATA) - 1
    
#     return TURRET_DATA[index]