import arcade
from map import Map
import time
import config


class MapViewer(arcade.Window):
    def __init__(self, game):
        self.game = game
        self.map: Map = game.map
        self.dimensions: tuple[int, int] = self.map.dimensions or (0, 0)
        self.tile_size: int = config.TILE_SIZE

        # Map area
        self.map_width: int = int(self.dimensions[0] * self.tile_size)
        self.map_height: int = int(self.dimensions[1] * self.tile_size)

        # Message box area
        self.message_box_height: int = config.MESSAGE_BOX_HEIGHT
        self.message_box_margin: int = config.MESSAGE_BOX_MARGIN

        # Total window size
        width: int = self.map_width
        height: int = self.map_height + self.message_box_height

        super().__init__(width, height, "GAME OF ORB")
        arcade.set_background_color(arcade.color.BLACK)

        # Message system
        self.messages: list[str] = []
        self.max_messages: int = config.MAX_MESSAGES  # Maximum visible messages

        # Timing system (delta-time based, non-blocking)
        self.tick_timer: float = 0.0
        self.tick_delay: float = config.TICK_DELAY

    def start(self):
        arcade.run()

    def on_update(self, delta_time):
        self.tick_timer += delta_time

        # Time for next tick?
        if self.tick_timer >= self.tick_delay:
            self.tick_timer = 0.0

            # Delegate to Game for logic processing
            if hasattr(self.game, "process_tick"):
                self.game.process_tick()

    def on_draw(self):
        self.clear()
        self.draw_map()
        self.draw_players()
        self.draw_meta_orb()
        self.draw_message_box()

    def draw_map(self):
        if self.map.tiles is None:
            return

        for y in range(self.map.tiles.shape[0]):
            for x in range(self.map.tiles.shape[1]):
                tile_type: str = self.map.tiles[y, x]
                color = config.COLORS[tile_type]["display_color"]

                pixel_x: int = x * self.tile_size
                # Map wird oberhalb der Message Box gezeichnet
                pixel_y: int = (
                    self.map.tiles.shape[0] - 1 - y
                ) * self.tile_size + self.message_box_height

                # Draw filled rectangle directly
                arcade.draw_lbwh_rectangle_filled(
                    pixel_x,  # Left
                    pixel_y,  # Bottom
                    self.tile_size - 1,  # Width (with 1px border)
                    self.tile_size - 1,  # Height (with 1px border)
                    color,
                )

    def draw_players(self):
        # Draw players if any (optional)
        if self.map.tiles is None:
            return

        player_position_data = self.game.get_player_positions()

        # Draw players
        for player in player_position_data:
            if player["team"] == "RED":
                pixel_x = (
                    player["position"][0] * self.tile_size + self.tile_size // 2
                )  # Center X
                pixel_y = (
                    (self.map.tiles.shape[0] - 1 - player["position"][1])
                    * self.tile_size
                    + self.tile_size // 2
                    + self.message_box_height
                )  # Center Y + message box offset
                arcade.draw_circle_filled(
                    pixel_x,
                    pixel_y,
                    self.tile_size // 3,
                    config.COLORS["RED_PLAYER"]["display_color"],  # Red player color
                )
                # Draw player name above the bubble
                arcade.draw_text(
                    player["name"],
                    pixel_x,
                    pixel_y + self.tile_size // 2,  # Above the bubble
                    arcade.color.WHITE,
                    font_size=max(8, self.tile_size // 4),  # Small font, minimum 8px
                    anchor_x="center",
                    anchor_y="bottom",
                )
            elif player["team"] == "BLU":
                pixel_x = (
                    player["position"][0] * self.tile_size + self.tile_size // 2
                )  # Center X
                pixel_y = (
                    (self.map.tiles.shape[0] - 1 - player["position"][1])
                    * self.tile_size
                    + self.tile_size // 2
                    + self.message_box_height
                )  # Center Y + message box offset
                arcade.draw_circle_filled(
                    pixel_x,
                    pixel_y,
                    self.tile_size // 3,
                    config.COLORS["BLUE_PLAYER"]["display_color"],  # Blue player color
                )
                # Draw player name above the bubble
                arcade.draw_text(
                    player["name"],
                    pixel_x,
                    pixel_y + self.tile_size // 2,  # Above the bubble
                    arcade.color.WHITE,
                    font_size=max(8, self.tile_size // 4),  # Small font, minimum 8px
                    anchor_x="center",
                    anchor_y="bottom",
                )

    def draw_meta_orb(self):
        """Draw the Meta Orb on the map"""
        if not hasattr(self.game, "meta_orb"):
            return

        if self.map.tiles is None:
            return

        meta_orb = self.game.meta_orb
        pixel_x = meta_orb.position[0] * self.tile_size + self.tile_size // 2
        pixel_y = (
            (self.map.tiles.shape[0] - 1 - meta_orb.position[1]) * self.tile_size
            + self.tile_size // 2
            + self.message_box_height
        )

        # Draw Meta Orb as a diamond/rhombus shape
        half_size = self.tile_size // 4

        # Diamond points: top, right, bottom, left
        points = [
            (pixel_x, pixel_y + half_size),  # Top
            (pixel_x + half_size, pixel_y),  # Right
            (pixel_x, pixel_y - half_size),  # Bottom
            (pixel_x - half_size, pixel_y),  # Left
        ]
        arcade.draw_polygon_filled(points, config.COLORS["META_ORB"]["display_color"])

    def draw_message_box(self):
        """Draw the message box at the bottom of the screen"""
        # Message box background
        arcade.draw_lbwh_rectangle_filled(
            0,  # Left
            0,  # Bottom
            self.map_width,  # Width
            self.message_box_height,  # Height
            (30, 30, 30),  # Dark gray background
        )

        # Message box border
        arcade.draw_lbwh_rectangle_outline(
            0, 0, self.map_width, self.message_box_height, arcade.color.WHITE, 2
        )

        # Draw messages
        font_size = 12
        line_height = 16
        start_y = self.message_box_height - self.message_box_margin - font_size

        # Show last N messages
        visible_messages = (
            self.messages[-self.max_messages :]
            if len(self.messages) > self.max_messages
            else self.messages
        )

        for i, message in enumerate(reversed(visible_messages)):
            y_pos = start_y - (i * line_height)
            if y_pos < self.message_box_margin:
                break  # Don't draw outside message box

            arcade.draw_text(
                message,
                self.message_box_margin,
                y_pos,
                arcade.color.WHITE,
                font_size=font_size,
            )

    def add_message(self, message: str):
        """Add a new message to the message box"""
        self.messages.append(message)
        print(f"[MESSAGE] {message}")  # Also print to console
