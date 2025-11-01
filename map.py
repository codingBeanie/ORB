import numpy as np
from PIL import Image
from PIL.Image import Image as PILImage

SOURCE_FOLDER: str = "assets/maps/"
COLOR_MAPPING: dict[tuple[int, int, int], str] = {
    (0, 0, 0): "WAL",  # WALL
    (255, 255, 255): "FLR",  # FLOOR
    (118, 66, 138): "ORS",  # ORB SPAWN
    (172, 50, 50): "RED",  # START RED
    (99, 155, 255): "BLU",  # START BLUE
}


class Map:
    def __init__(self, map_name: str):
        self.name: str = map_name
        self.image: PILImage | None = None
        self.image_data: np.ndarray | None = None
        self.tiles: np.ndarray | None = None
        self.dimensions: tuple[int, int] | None = None

        self.load_image()
        self.extract_image_data()

    def load_image(self):
        try:
            self.image = Image.open(SOURCE_FOLDER + self.name + ".png")
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Map image for '{self.name}' not found in {SOURCE_FOLDER}."
            )

    def extract_image_data(self):
        self.image_data = np.array(self.image)
        self.tiles = np.zeros(self.image_data.shape[:2], dtype="U3")
        self.dimensions = (self.image_data.shape[1], self.image_data.shape[0])

        for x in range(self.image_data.shape[1]):
            for y in range(self.image_data.shape[0]):
                pixel_rgb: np.ndarray = self.image_data[y, x]
                tile_type: str | None = COLOR_MAPPING.get(tuple(pixel_rgb))
                if tile_type:
                    self.tiles[y, x] = tile_type
                else:
                    self.tiles[y, x] = "???"

    def get_spawning_positions(self, team_code: str) -> list[tuple[int, int]]:
        """Get all spawn positions for a specific team"""
        if self.tiles is None:
            return []

        positions = np.argwhere(self.tiles == team_code)
        print(positions)
        return [(pos[1], pos[0]) for pos in positions]

    def get_meta_orb_spawn_position(self) -> tuple[int, int]:
        """Get the spawn position for the Meta Orb"""
        if self.tiles is None:
            return (0, 0)

        positions = np.argwhere(self.tiles == "ORS")
        if positions.size == 0:
            return (0, 0)  # Default position if none found

        pos = positions[0]
        return (pos[1], pos[0])
