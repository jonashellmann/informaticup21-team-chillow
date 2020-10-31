import logging
from typing import List, Tuple

from chillow.exceptions import InvalidPlayerMoveException, PlayerSpeedNotInRangeException, \
    PlayerOutsidePlaygroundException
from chillow.model.game import Game
from chillow.model.action import Action
from chillow.model.player import Player
from chillow.model.direction import Direction
from chillow.model.turn import Turn


class GameService:

    def __init__(self, game: Game):
        self.game = game
        self.turn = Turn(self.game.players, game.deadline)
        self.visited_cells_by_player = {}

    def do_action(self, player: Player, action: Action):
        try:
            new_turn = self.turn.action(player)
            self.visited_cells_by_player[player.id] = self.get_and_visit_cells(player, action)

            if new_turn:
                self.check_and_set_died_players()

        except InvalidPlayerMoveException:
            self.set_player_inactive(player)

        self.game.running = self.is_game_running()

    def check_and_set_died_players(self):
        for row in range(len(self.game.cells)):
            for col in range(len(self.game.cells[row])):
                cell = self.game.cells[row][col]
                if cell.players is not None and len(cell.players) > 1:
                    for player_id, cells in self.visited_cells_by_player.items():
                        for cell in cells:
                            if cell[0] == col and cell[1] == row:
                                for player in self.game.players:
                                    if player_id == player.id:
                                        self.set_player_inactive(player)
                                        logging.debug("Player with id " + str(player.id)
                                                      + " had a collision and is inactive now")

    def is_game_running(self) -> bool:
        active_player_ctr = 0
        for player in self.game.players:
            if player.active:
                active_player_ctr += 1
        return active_player_ctr >= 2

    @staticmethod
    def get_horizontal_and_vertical_multiplier(player: Player) -> Tuple[int, int]:
        vertical_multiplier = 0
        horizontal_multiplier = 0
        if player.direction == Direction.up:
            vertical_multiplier = -1
        elif player.direction == Direction.down:
            vertical_multiplier = 1
        elif player.direction == Direction.left:
            horizontal_multiplier = -1
        elif player.direction == Direction.right:
            horizontal_multiplier = 1

        return horizontal_multiplier, vertical_multiplier

    def get_and_visit_cells(self, player: Player, action: Action) -> List[Tuple[int, int]]:
        visited_cells = []

        GameService.change_player_status_by_action(player, action)

        horizontal_multiplier, vertical_multiplier = GameService.get_horizontal_and_vertical_multiplier(player)

        for i in range(0, player.speed):
            visited_cells.append(
                (player.x + (i + 1) * horizontal_multiplier, player.y + (i + 1) * vertical_multiplier))

        if self.turn.turn_ctr % 6 == 0 and len(visited_cells) > 1:  # Lücke, also nur die erste und letzte Punkt nehmen
            visited_cells = [visited_cells[0], visited_cells[-1]]

        visited_cells_result = []
        for (x, y) in visited_cells:
            if x not in range(self.game.width) or y not in range(self.game.height):
                raise PlayerOutsidePlaygroundException(player)
            player.x = x
            player.y = y
            visited_cells_result.append((x, y))
            if self.game.cells[y][x].players is None:
                self.game.cells[y][x].players = [player]
            else:
                self.game.cells[y][x].players.append(player)
                break

        return visited_cells_result

    @staticmethod
    def change_player_status_by_action(player: Player, action: Action):
        if action == action.turn_left:
            if player.direction == Direction.up:
                player.direction = Direction.left
            elif player.direction == Direction.left:
                player.direction = Direction.down
            elif player.direction == Direction.down:
                player.direction = Direction.right
            elif player.direction == Direction.right:
                player.direction = Direction.up
        elif action == action.turn_right:
            if player.direction == Direction.up:
                player.direction = Direction.right
            elif player.direction == Direction.right:
                player.direction = Direction.down
            elif player.direction == Direction.down:
                player.direction = Direction.left
            elif player.direction == Direction.left:
                player.direction = Direction.up
        elif action == action.speed_up:
            player.speed += 1
        elif action == action.slow_down:
            player.speed -= 1

        if player.speed not in range(1, 11):
            raise PlayerSpeedNotInRangeException(player)

    def set_player_inactive(self, player: Player):
        if player in self.turn.playersWithPendingAction:
            self.turn.playersWithPendingAction.remove(player)
        player.active = False
