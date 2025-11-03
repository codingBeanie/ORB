from map import Map
from ai.strategy import Strategy


class Player:
    def __init__(self, name: str, team: str, strategy: Strategy | None = None):
        self.name = name
        self.team = team
        self.display_color = (255, 0, 0) if team == "RED" else (0, 0, 255)
        self.strategy = strategy

    def take_action(self, map: Map):
        """ask strategy for next actions"""
        if self.strategy:
            action_list = self.strategy.get_actions(self, map)
            print(f"Player {self.name} actions: {action_list}")

            # choose first action for now
            if action_list:
                if "move" in action_list[0]:
                    self.move_to(map, action_list[0]["move"])

    def move_to(self, map, new_position: tuple[int, int]):
        """Update player position (to be called by Game)"""
        # get current position
        current_position = map.get_position_of_player(self)
        current_field = map.get_field_by_coordinates(
            current_position[0], current_position[1]
        )

        if current_position is None:
            return  # Player not on the map

        # update player position
        new_field = map.get_field_by_coordinates(new_position[0], new_position[1])

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
                f"Player {self.name} cannot move to {new_position}: occupied by another player {new_field.player.name}"
            )
            return

        # move player to new field
        new_field.player = self

        # reset current field
        if current_field is not None:
            current_field.player = None
