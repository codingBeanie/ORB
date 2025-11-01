from map import Map
from player import Player
from viewer import MapViewer
from meta_orb import MetaOrb
import config


class Game:
    def __init__(
        self,
        map_name: str,
        players_red: list[Player] | None = None,
        players_blue: list[Player] | None = None,
    ):
        self.map = Map(map_name)
        self.players_red = players_red or []
        self.players_blue = players_blue or []
        self.player_list = []
        self.running = False
        self.tick = 0
        self.score_red = 0
        self.score_blue = 0

        # Interleave red and blue players
        max_players = max(len(self.players_red), len(self.players_blue))
        for i in range(max_players):
            if i < len(self.players_red):
                self.player_list.append(self.players_red[i])
            if i < len(self.players_blue):
                self.player_list.append(self.players_blue[i])

    def spawn_players(self):
        """Spawn all players on the map"""
        red_spawn_points = self.map.get_coordinates_by_tile_name("RED_SPAWN")
        blue_spawn_points = self.map.get_coordinates_by_tile_name("BLUE_SPAWN")

        for i, player in enumerate(self.players_red):
            player.position = red_spawn_points[i]

        for i, player in enumerate(self.players_blue):
            player.position = blue_spawn_points[i]

    def run_game_loop(self):
        self.running = True
        # Create viewer and pass self - viewer will call process_tick()
        self.viewer = MapViewer(self)
        self.viewer.start()

    def process_tick(self):
        """Called by viewer every tick - handles all game logic"""
        self.tick += 1
        if not self.running:
            return

        if self.tick > config.MAX_TICKS and self.running:
            self.running = False
            if hasattr(self, "viewer"):
                self.viewer.add_message("Game finished!")
                return

        # Game continues
        if hasattr(self, "viewer"):
            self.viewer.add_message(f"Tick {self.tick}: Game continues...")
