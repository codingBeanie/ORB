TEAM_MAPPING = {
    "RED": "RED",
    "BLUE": "BLU",
}


class Player:
    def __init__(self, name: str, team: str):
        self.name = name
        self.team = team
        self.team_code = TEAM_MAPPING.get(team.upper(), "???")
        self.position = (0, 0)

    def spawn(self, map):
        pass
