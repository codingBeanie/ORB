import numpy as np
from PIL import Image
from PIL.Image import Image as PILImage
import config
import entities


class Map:
    def __init__(self, map_name: str):
        self.name: str = map_name
        self.image: PILImage | None = None
        self.image_data: np.ndarray | None = None
        self.image_dimensions: tuple[int, int] | None = None

        self.fields: list[entities.Field] = []

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
                pixel_rgb: np.ndarray = self.image_data[y, x]
                tile: entities.Tile = entities.get_tile_by_color(tuple(pixel_rgb))
                field = entities.Field(x=x, y=height - 1 - y, tile=tile)
                self.fields.append(field)

    def get_coordinates_by_tile_name(self, tile_name: str) -> list[tuple[int, int]]:
        """Get all coordinates of fields with a specific tile name"""
        positions = []
        for field in self.fields:
            if field.tile.name == tile_name:
                positions.append((field.x, field.y))
        return positions
