from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_objects.player import Player
    from map import Map


class Strategy:
    """Base Strategy class"""

    def __init__(self):
        pass

    def get_actions(self, player, map):
        """Override this method in subclasses to define specific strategies"""
        raise NotImplementedError("Subclasses must implement get_actions method")


class StrategyStraightOrb(Strategy):
    """Strategy: Get straight to the orb, catch it or attack the player who has it.
    Bring it back to base on fastest path."""

    def __init__(self):
        super().__init__()

    def get_actions(self, player: Player, map: Map):
        action_list = []
        # get current position
        player_position = map.get_position_of_player(player)

        # define target position
        target_position = map.position_orb

        # create move action towards target
        if target_position is not None and player_position is not None:
            next_move = map.find_next_move_to_target(player_position, target_position)
            if next_move is not None:
                action = {"move": next_move}
                action_list.append(action)

        return action_list
