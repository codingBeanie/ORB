from dataclasses import dataclass


@dataclass
class Tile:
    name: str
    import_color: tuple[int, int, int] | None
    display_color: tuple[int, int, int] | None
    passable: bool


@dataclass
class GameObject:
    name: str
    display_color: tuple[int, int, int]


@dataclass
class Field:
    x: int
    y: int
    tile: Tile
    game_object: GameObject | None = None


TILES = [
    Tile("WALL", (0, 0, 0), (50, 50, 50), passable=False),
    Tile("FLOOR", (255, 255, 255), (200, 200, 200), passable=True),
    Tile("ORB_SPAWN", (118, 66, 138), (118, 66, 138), passable=True),
    Tile("RED_SPAWN", (172, 50, 50), (172, 50, 50), passable=True),
    Tile("BLUE_SPAWN", (99, 155, 255), (99, 155, 255), passable=True),
    Tile("UNKNOWN", None, None, passable=False),
]

GAME_OBJECTS = [
    GameObject("META_ORB", (130, 80, 200)),
    GameObject("RED_PLAYER", (255, 0, 0)),
    GameObject("BLUE_PLAYER", (0, 0, 255)),
]


def get_tile_by_color(color: tuple[int, int, int]) -> Tile:
    """Find the first Tile with the given import color"""
    for tile in TILES:
        if tile.import_color == color:
            return tile
    return TILES[-1]


def get_color_by_game_object_name(name: str) -> tuple[int, int, int]:
    """Get the display color of a GameObject by its name"""
    for obj in GAME_OBJECTS:
        if obj.name == name:
            return obj.display_color
    return (128, 128, 128)  # Default gray if not found
