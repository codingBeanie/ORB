import arcade
from map import Map

# Colors for rendering
TILE_COLORS = {
    "WAL": (50, 50, 50),
    "FLR": (200, 200, 200),
    "ORB": (118, 66, 138),
    "RED": (172, 50, 50),
    "BLU": (99, 155, 255),
    "???": (255, 0, 255),
}


class MapViewer(arcade.Window):
    def __init__(self, game, tile_size: int = 20):
        self.game = game
        self.map: Map = game.map
        self.dimensions: tuple[int, int] = self.map.dimensions or (0, 0)
        self.tile_size: int = tile_size

        width: int = int(self.dimensions[0] * self.tile_size)
        height: int = int(self.dimensions[1] * self.tile_size)

        super().__init__(width, height, "GAME OF ORB")
        arcade.set_background_color(arcade.color.BLACK)

    def start(self):
        arcade.run()

    def on_draw(self):
        self.clear()

        if self.map.tiles is None:
            return

        for y in range(self.map.tiles.shape[0]):
            for x in range(self.map.tiles.shape[1]):
                tile_type: str = self.map.tiles[y, x]
                color = TILE_COLORS.get(tile_type, (255, 0, 255))

                pixel_x: int = x * self.tile_size
                pixel_y: int = (self.map.tiles.shape[0] - 1 - y) * self.tile_size

                # Draw filled rectangle directly
                arcade.draw_lbwh_rectangle_filled(
                    pixel_x,  # Left
                    pixel_y,  # Bottom
                    self.tile_size - 1,  # Width (with 1px border)
                    self.tile_size - 1,  # Height (with 1px border)
                    color,
                )

                # Draw players if any (optional)
                player_positions = self.game.get_player_positions()
                team_red_positions = player_positions.get("RED", [])
                team_blue_positions = player_positions.get("BLU", [])
                # team "RED"
                for player_position in team_red_positions:
                    if player_position == (x, y):
                        arcade.draw_circle_filled(
                            pixel_x + self.tile_size // 2,
                            pixel_y + self.tile_size // 2,
                            self.tile_size // 4,
                            arcade.color.RED,
                        )
                # team "BLU"
                for player_position in team_blue_positions:
                    if player_position == (x, y):
                        arcade.draw_circle_filled(
                            pixel_x + self.tile_size // 2,
                            pixel_y + self.tile_size // 2,
                            self.tile_size // 4,
                            arcade.color.BLUE,
                        )
