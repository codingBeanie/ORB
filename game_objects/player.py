import random


class Player:
    def __init__(self, name: str, team: str):
        self.name = name
        self.team = team
        self.display_color = (255, 0, 0) if team == "RED" else (0, 0, 255)

    def take_action(self, possible_moves: list[tuple[int, int]]):
        """Choose an action from possible moves. Currently selects randomly."""
        pass
