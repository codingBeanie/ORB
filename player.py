class Player:
    def __init__(self, name: str, team: str):
        self.name = name
        self.team = team
        self.position: tuple[int, int] = (0, 0)

    def spawn(self, map):
        pass
