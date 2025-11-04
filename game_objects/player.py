from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from arena import Arena
    from game import Game
    from ai.strategy import Strategy


class Player:
    def __init__(self, name: str, team: str, strategy: Strategy | None = None):
        self.name = name
        self.team = team
        self.display_color = (255, 0, 0) if team == "RED" else (0, 0, 255)
        self.strategy = strategy

    def take_action(self, arena: Arena, game: Game):
        """ask strategy for next actions"""
        if self.strategy:
            action = self.strategy.get_action(self, arena)
            print(f"Player {self.name} actions: {action}")

            # choose first action for now
            if action:
                if "move" in action:
                    self.move_to(arena, action["move"])

                if "pick_up" in action:
                    self.pick_up(arena)
                    game.game_messages.append(
                        f"Player {self.name} picked up the Meta Orb"
                    )

    def move_to(self, arena: Arena, new_position: tuple[int, int]):
        """Update player position (to be called by Game)"""
        # get current position
        current_position = arena.get_position_of_player(self)

        if current_position is None:
            return  # Player not on the map

        current_field = arena.get_field_by_coordinates(
            current_position[0], current_position[1]
        )

        # update player position
        new_field = arena.get_field_by_coordinates(new_position[0], new_position[1])

        # out of bounds
        if new_field is None:
            print(f"Player {self.name} cannot move to {new_position}: out of bounds")
            return

        # not passable
        if not new_field.tile.passable:
            print(f"Player {self.name} cannot move to {new_position}: not passable")
            return

        # occupied by another player
        if new_field.player:
            print(
                f"Player {self.name} cannot move to {new_position}: occupied by another player {new_field.player.name}. Try to move elsewhere."
            )
            possible_moves = arena.get_passable_adjacent_positions(current_position)
            if possible_moves:
                new_field = arena.get_field_by_coordinates(
                    possible_moves[0][0], possible_moves[0][1]
                )
            else:
                return

        if new_field is None:
            return  # no valid move found

        # move player to new field
        new_field.player = self

        # if orb is carried by this player, update its position
        meta_orb = arena.get_meta_orb_object()
        if meta_orb and meta_orb.carried_by == self:
            arena.change_meta_orb_position(new_position)

        # reset current field
        if current_field is not None:
            current_field.player = None

    def pick_up(self, map: Arena):
        """Pick up Meta Orb if on the same field and not already carried"""
        current_position = map.get_position_of_player(self)
        if current_position is None:
            print(f"Player {self.name} cannot pick up orb: not on the map")
            return

        current_field = map.get_field_by_coordinates(
            current_position[0], current_position[1]
        )

        if current_field and current_field.meta_orb:
            meta_orb = current_field.meta_orb

            if meta_orb.carried_by is not None:
                print(
                    f"Player {self.name} cannot pick up orb: already carried by {meta_orb.carried_by.name}"
                )
                return
            meta_orb.carried_by = self
            meta_orb.carried = True  # type:ignore
            print(f"Player {self.name} picked up the Meta Orb")
        else:
            print(f"Player {self.name} cannot pick up orb: no orb on the field")
