from game import Game
from player import Player

PLAYERS_RED = ["Alice", "Bob", "Eve"]
PLAYERS_BLUE = ["Charlie", "Diana", "Frank"]

# specify map name
test_map_name: str = "the_petting_zoo"

players_red: list[Player] = []
for player in PLAYERS_RED:
    players_red.append(Player(player, "RED"))

players_blue: list[Player] = []
for player in PLAYERS_BLUE:
    players_blue.append(Player(player, "BLUE"))

game = Game(test_map_name, players_red, players_blue)
game.spawn_players()
game.spawn_orbs()
game.run_game_loop()
