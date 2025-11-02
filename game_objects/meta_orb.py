from game_objects.player import Player


class MetaOrb:
    def __init__(self, carried_by: Player | None = None):
        self.name = "META_ORB"
        self.display_color = (130, 80, 200)
        self.carried = None
        self.carried_by = carried_by
