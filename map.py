import numpy as np
from PIL import Image
from PIL.Image import Image as PILImage
import config
import game_objects.entities as entities
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


class Map:
    def __init__(self, map_name: str):
        self.name: str = map_name
        self.image: PILImage | None = None
        self.image_data: np.ndarray | None = None
        self.image_dimensions: tuple[int, int] | None = None

        self.fields: list[entities.Field] = []
        self.position_orb: tuple[int, int] | None = None
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

    def get_possible_moves(
        self, position: tuple[int, int]
    ) -> list[tuple[int, int]] | None:
        """Get all possible move coordinates from a given position"""
        x, y = position
        possible_moves = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        ]
        positions = []
        for move in possible_moves:
            for field in self.fields:
                if field.x == move[0] and field.y == move[1]:  # get field

                    # field is not passable
                    if not field.tile.passable:
                        break

                    # field is occupied by another player
                    if field.player is not None:
                        break

                    positions.append(move)
        return positions
