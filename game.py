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
        self.running = False
        self.tick = 0
        self.score_red = 0
        self.score_blue = 0

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

        # iterate players and give them context
        for player in self.players:
            pass

    def spawn_players(self):
        red_spawns = self.map.get_spawning_positions("RED_SPAWN")
        blue_spawns = self.map.get_spawning_positions("BLUE_SPAWN")

        for player in self.players_red:
            player.position = red_spawns.pop(0)

        for player in self.players_blue:
            player.position = blue_spawns.pop(0)

        self.players = [
            item for pair in zip(self.players_red, self.players_blue) for item in pair
        ]

    def spawn_orbs(self):
        meta_orb_position = self.map.get_meta_orb_spawn_position()
        self.meta_orb = MetaOrb(meta_orb_position)

    def get_player_positions(self) -> list[dict]:
        position_data = []

        for player in self.players_red:
            position_data.append(
                {"team": player.team, "name": player.name, "position": player.position}
            )

        for player in self.players_blue:
            position_data.append(
                {"team": player.team, "name": player.name, "position": player.position}
            )

        return position_data
