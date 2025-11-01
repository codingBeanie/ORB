# GAME CONFIGURATION
TICK_DELAY = 0.1
MAX_TICKS = 100

# TEAM SETTINGS
PLAYERS_RED = ["Alice", "Bob", "Eve"]
PLAYERS_BLUE = ["Charlie", "Diana", "Frank"]

# MAP SETTINGS
SOURCE_FOLDER: str = "assets/maps/"

# COLOR SETTINGS
COLORS = {
    "WALL": {"import_color": (0, 0, 0), "display_color": (50, 50, 50)},
    "FLOORS": {"import_color": (255, 255, 255), "display_color": (200, 200, 200)},
    "ORB_SPAWN": {"import_color": (118, 66, 138), "display_color": (118, 66, 138)},
    "META_ORB": {"import_color": (130, 80, 200), "display_color": (130, 80, 200)},
    "RED_SPAWN": {"import_color": (172, 50, 50), "display_color": (172, 50, 50)},
    "BLUE_SPAWN": {"import_color": (99, 155, 255), "display_color": (99, 155, 255)},
    "RED_PLAYER": {"import_color": None, "display_color": (255, 0, 0)},
    "BLUE_PLAYER": {"import_color": None, "display_color": (0, 0, 255)},
    "UNKNOWN": {"import_color": None, "display_color": (255, 0, 255)},
}


def get_name_by_import_color(import_color: tuple[int, int, int]) -> str | None:
    for name, color_info in COLORS.items():
        if color_info["import_color"] == import_color:
            return name
    return None


# UI SETTINGS
TILE_SIZE = 30
MESSAGE_BOX_HEIGHT = 120
MESSAGE_BOX_MARGIN = 10
MAX_MESSAGES = 6
