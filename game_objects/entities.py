from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_objects.meta_orb import MetaOrb
    from game_objects.player import Player


@dataclass
class Tile:
    name: str
    import_color: tuple[int, int, int] | None
    display_color: tuple[int, int, int]
    passable: bool


@dataclass
class Field:
    x: int
    y: int
    tile: Tile
    player: Player | None = None
    meta_orb: MetaOrb | None = None


TILES = [
    Tile("WALL", (0, 0, 0), (50, 50, 50), passable=False),
    Tile("FLOOR", (255, 255, 255), (200, 200, 200), passable=True),
    Tile("ORB_SPAWN", (118, 66, 138), (118, 66, 138), passable=True),
    Tile("RED_SPAWN", (172, 50, 50), (172, 50, 50), passable=True),
    Tile("BLUE_SPAWN", (99, 155, 255), (99, 155, 255), passable=True),
    Tile("UNKNOWN", None, (0, 0, 0), passable=False),
]


def get_tile_by_color(color: tuple[int, int, int]) -> Tile:
    """Find the first Tile with the given import color"""
    for tile in TILES:
        if tile.import_color == color:
            return tile
    return TILES[-1]
