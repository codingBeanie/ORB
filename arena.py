import numpy as np
from PIL import Image
from PIL.Image import Image as PILImage
import config
import game_objects.entities as entities
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from game_objects.meta_orb import MetaOrb


class Arena:
    def __init__(self, map_name: str):
        self.name: str = map_name
        self.image: PILImage | None = None
        self.image_data: np.ndarray | None = None
        self.image_dimensions: tuple[int, int] | None = None

        self.fields: list[entities.Field] = []
        self.positions_red_spawn: list[tuple[int, int]] = []
        self.positions_blue_spawn: list[tuple[int, int]] = []
        self.pathfinding_matrix: np.ndarray | None = None
        self.pathfinding_grid: Grid | None = None

        self.load_image()
        self.extract_image_data()

    def load_image(self):
        try:
            self.image = Image.open(config.SOURCE_FOLDER + self.name + ".png")
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Map image for '{self.name}' not found in {config.SOURCE_FOLDER}."
            )

    def extract_image_data(self):
        self.image_data = np.array(self.image)
        self.tiles = np.empty(self.image_data.shape[:2], dtype=entities.Tile)
        self.image_dimensions = (self.image_data.shape[1], self.image_data.shape[0])
        self.fields = []

        height, width = self.image_data.shape[:2]

        for y in range(height):
            for x in range(width):
                # adjust y coordinate
                adjusted_y = height - 1 - y
                # fill the fields list
                pixel_rgb: np.ndarray = self.image_data[y, x]
                tile: entities.Tile = entities.get_tile_by_color(tuple(pixel_rgb))
                field = entities.Field(x=x, y=adjusted_y, tile=tile)
                self.fields.append(field)

                # fill the pathfinding matrix
                if self.pathfinding_matrix is None:
                    self.pathfinding_matrix = np.zeros((height, width), dtype=int)

                self.pathfinding_matrix[adjusted_y, x] = 1 if tile.passable else 0

        # create pathfinding grid
        if self.pathfinding_matrix is not None:
            self.pathfinding_grid = Grid(matrix=self.pathfinding_matrix)

    def get_positions_by_tile_name(self, tile_name: str) -> list[tuple[int, int]]:
        """Get all coordinates of fields with a specific tile name"""
        positions = []
        for field in self.fields:
            if field.tile and field.tile.name == tile_name:
                positions.append((field.x, field.y))
        return positions

    def get_position_of_player(self, player):
        """Get the coordinates of the field where the specified player is located"""
        for field in self.fields:
            if field.player == player:
                return (field.x, field.y)
        return None

    def get_field_by_coordinates(self, x: int, y: int) -> entities.Field | None:
        """Get the field at specific coordinates"""
        for field in self.fields:
            if field.x == x and field.y == y:
                return field
        return None

    def find_next_move_to_target(
        self, start: tuple[int, int], end: tuple[int, int]
    ) -> tuple[int, int] | None:
        """Find the shortest path from start to end using A* algorithm"""
        if self.pathfinding_grid is None:
            return None

        if start == end:
            return None

        start_node = self.pathfinding_grid.node(start[0], start[1])
        end_node = self.pathfinding_grid.node(end[0], end[1])

        finder = AStarFinder()
        path, _ = finder.find_path(start_node, end_node, self.pathfinding_grid)
        next_step = path[1] if len(path) > 1 else None

        if not path:
            return None

        # convert path to list of tuples
        next_step_position = (next_step.x, next_step.y)  # type: ignore
        return next_step_position

    def get_meta_orb_position(self) -> tuple[int, int] | None:
        """Get the current position of the Meta Orb on the map"""
        for field in self.fields:
            if field.meta_orb is not None:
                return (field.x, field.y)
        return None

    def change_meta_orb_position(self, new_position: tuple[int, int]) -> None:
        """Change the position of the Meta Orb on the map"""
        meta_orb = self.get_meta_orb_object()
        # First, remove the orb from its current position
        for field in self.fields:
            if field.meta_orb is not None:
                field.meta_orb = None
                break

        # Then, place the orb at the new position
        field = self.get_field_by_coordinates(new_position[0], new_position[1])
        if field is not None:
            field.meta_orb = meta_orb

    def get_meta_orb_object(self) -> MetaOrb | None:
        """Get the current status of the Meta Orb on the map"""
        for field in self.fields:
            if field.meta_orb is not None:
                return field.meta_orb
        return None

    def get_passable_adjacent_positions(
        self, position: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """Get all passable adjacent positions (up, down, left, right) from a given position"""
        x, y = position
        adjacent_positions = [
            (x, y + 1),  # Up
            (x, y - 1),  # Down
            (x - 1, y),  # Left
            (x + 1, y),  # Right
        ]
        passable_positions = []
        for pos in adjacent_positions:
            field = self.get_field_by_coordinates(pos[0], pos[1])
            if field and field.tile.passable and field.player is None:
                passable_positions.append(pos)
        return passable_positions
