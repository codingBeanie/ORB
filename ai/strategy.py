from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from arena import Arena
    from player import Player  # type: ignore


class Strategy:
    """Base Strategy class"""

    def __init__(self):
        pass

    def get_action(self, player: Player, arena: Arena):
        """Override this method in subclasses to define specific strategies"""
        raise NotImplementedError("Subclasses must implement get_actions method")


class StrategyStraightOrb(Strategy):
    """Strategy: Get straight to the orb, catch it or attack the player who has it.
    Bring it back to base on fastest path."""

    def __init__(self):
        super().__init__()

    def get_action(self, player: Player, arena: Arena):
        action = {}
        meta_orb = arena.get_meta_orb_object()
        meta_orb_position = arena.get_meta_orb_position()
        player_position = arena.get_position_of_player(player)

        if meta_orb is None:
            return action  # no orb on the map

        """ Meta Orb is carried by someone """
        if meta_orb.carried_by is not None:

            # The opponent has the orb
            if meta_orb.carried_by.team != player.team:
                # move towards the player who has the orb
                action = move_towards_meta_orb(arena, player)
                return action

            # We have the orb
            else:
                # move towards our spawn point
                spawn_tile_name = "RED_SPAWN" if player.team == "RED" else "BLUE_SPAWN"
                spawn_positions = arena.get_positions_by_tile_name(spawn_tile_name)
                if spawn_positions:
                    target_position = spawn_positions[0]
                    if player_position is not None:
                        next_move = arena.find_next_move_to_target(
                            player_position, target_position
                        )
                        if next_move is not None:
                            action = {"move": next_move}
                            return action

        """ Meta Orb is on the ground """
        """ You can pick it up """
        if meta_orb_position == player_position and meta_orb.carried_by is None:
            action = {"pick_up": True}
            return action
        else:
            """move towards the meta orb"""
            action = move_towards_meta_orb(arena, player)
            return action


def move_towards_meta_orb(arena: Arena, player: Player):
    # get current position
    player_position = arena.get_position_of_player(player)

    # define target position
    target_position = arena.get_meta_orb_position()

    # create move action towards target
    if target_position is not None and player_position is not None:
        next_move = arena.find_next_move_to_target(player_position, target_position)
        if next_move is not None:
            action = {"move": next_move}
            return action
