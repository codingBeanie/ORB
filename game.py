from map import Map
from player import Player
from viewer import MapViewer


class Game:
    def __init__(
        self, map_name: str, players_red: list = [Player], players_blue: list = [Player]
    ):
        self.map = Map(map_name)
        self.players_red = players_red
        self.players_blue = players_blue

    def show_map(self, tile_size: int = 20):
        viewer = MapViewer(self, tile_size)
        viewer.start()

    def spawn_players(self):
        red_spawns = self.map.get_spawning_positions("RED")
        blue_spawns = self.map.get_spawning_positions("BLU")

        for player in self.players_red:
            player.position = red_spawns.pop(0)

        for player in self.players_blue:
            player.position = blue_spawns.pop(0)

    def get_player_positions(self) -> dict[str, list[tuple[int, int]]]:
        positions = {"RED": [], "BLU": []}

        for player in self.players_red:
            positions["RED"].append(player.position)

        for player in self.players_blue:
            positions["BLU"].append(player.position)

        return positions
