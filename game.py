from map import Map
from player import Player
from viewer import MapViewer
from meta_orb import MetaOrb
import time
import arcade

TICK_DELAY = 0.1
MAX_TICKS = 100


class Game:
    def __init__(
        self, map_name: str, players_red: list = [Player], players_blue: list = [Player]
    ):
        self.map = Map(map_name)
        self.players_red = players_red
        self.players_blue = players_blue
        self.running = False
        self.tick = 0
        self.score_red = 0
        self.score_blue = 0

    def run_game_loop(self):
        self.running = True
        # Create viewer and pass self - viewer will call process_tick()
        self.viewer = MapViewer(self, tile_size=30, tick_delay=TICK_DELAY)
        self.viewer.start()

    def process_tick(self):
        """Called by viewer every tick - handles all game logic"""
        self.tick += 1
        if not self.running:
            return

        if self.tick > MAX_TICKS and self.running:
            self.running = False
            if hasattr(self, "viewer"):
                self.viewer.add_message("Game finished!")
                return

        # Game continues
        if hasattr(self, "viewer"):
            self.viewer.add_message(f"Tick {self.tick}: Game continues...")

        # Here you can add all your game logic:
        # - Process player actions
        # - Update game state
        # - Check win conditions
        # - etc.

    def spawn_players(self):
        red_spawns = self.map.get_spawning_positions("RED")
        blue_spawns = self.map.get_spawning_positions("BLU")

        for player in self.players_red:
            player.position = red_spawns.pop(0)

        for player in self.players_blue:
            player.position = blue_spawns.pop(0)

    def spawn_orbs(self):
        meta_orb_position = self.map.get_meta_orb_spawn_position()
        self.meta_orb = MetaOrb(meta_orb_position)

    def get_player_positions(self) -> list[dict]:
        position_data = []

        for player in self.players_red:
            position_data.append(
                {"team": "RED", "name": player.name, "position": player.position}
            )

        for player in self.players_blue:
            position_data.append(
                {"team": "BLU", "name": player.name, "position": player.position}
            )

        return position_data
