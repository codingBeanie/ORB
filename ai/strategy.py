class StrategyStraightOrb:
    """Strategy: Get straight to the orb, catch it or attack the player who has it.
    Bring it back to base on fastest path."""

    def __init__(self):
        pass

    def decide_action(self, map, player):
        # information about player
        player_position = player.position

        # map information
