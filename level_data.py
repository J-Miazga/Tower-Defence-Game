LEVEL_DATA = {
    # Level 1 progression details
    1: {
        "map": "maps/level2.txt",  # File path for the next level's map
        "story": (
            "Zwiad meldował większe siły niż przewidywaliśmy. "
            "Wróg zaczyna używać ciężkiego sprzętu. Nasze wieżyczki z minigunami dają radę, "
            "ale to już nie są zwykłe potyczki. To wojna na pełną skalę."
        ),
        "reset_turrets": True,         # Remove all existing turrets before this level
        "set_mission": "Upgrade Tower" # Mission objective for this level
    },

    # Level 2 progression details
    2: {
        "map": "maps/level3.txt",  # File path for the next level's map
        "story": (
            "To już ostatnia linia obrony. Jeśli ją stracimy, wszystko przepada. "
            "Zyskaliśmy trochę czasu dzięki rakietowym wieżyczkom, ale wróg rzuca wszystko, co ma. "
            "Przygotujcie się – nie będzie odwrotu."
        ),
        "reset_turrets": True,
        "set_mission": "Upgrade Tower"
    },

    # Final level: end of the game
    3: {
        "story": (
            "Udało się. Obroniliśmy bazę, a wróg się wycofuje. "
            "Straty są duże, ale pokazaliśmy, że nie damy się złamać. "
            "Teraz my przechodzimy do ataku."
        ),
        "end_game": True,              # Marks the end of the game
        "set_mission": "Upgrade Tower"
    }
}
