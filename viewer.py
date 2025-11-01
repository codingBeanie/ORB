import arcade
from map import Map
import time
import config
import entities


class MapViewer(arcade.Window):
    def __init__(self, game):
        self.game = game
        self.fields: list[entities.Field] = game.map.fields
        self.dimensions: tuple[int, int] = game.map.image_dimensions or (0, 0)
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
        if self.fields is None:
            return

        for field in self.fields:
            pixel_x: int = field.x * self.tile_size
            pixel_y: int = field.y * self.tile_size + self.message_box_height

            # Draw filled rectangle directly
            arcade.draw_lbwh_rectangle_filled(
                pixel_x,  # Left
                pixel_y,  # Bottom
                self.tile_size - 1,  # Width (with 1px border)
                self.tile_size - 1,  # Height (with 1px border)
                field.tile.display_color or (128, 128, 128),  # Default gray if None
            )

    def draw_players(self):
        # Draw players
        if self.fields is None:
            return
        pass

    def draw_meta_orb(self):
        """Draw the Meta Orb on the map"""
        pass

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
