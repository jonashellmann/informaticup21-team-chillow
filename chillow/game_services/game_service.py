from typing import List, Tuple

from chillow.game_services.exceptions import MultipleActionByPlayerError, DeadLineExceededException, \
    PlayerSpeedNotInRangeException, PlayerOutsidePlaygroundException
from chillow.model.game import Game
from chillow.model.action import Action
from chillow.model.player import Player
from chillow.model.direction import Direction
from chillow.game_services.turn import Turn


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

        except (MultipleActionByPlayerError, DeadLineExceededException, PlayerSpeedNotInRangeException,
                PlayerOutsidePlaygroundException):
            self.set_player_inactive(player)

        self.game.running = self.is_game_running()

    def check_and_set_died_players(self):
        for row in range(len(self.game.cells)):
            for col in range(len(self.game.cells[row])):
                cell = self.game.cells[row][col]
                if cell.players is not None and len(cell.players) > 1:
                    for player_id, cells in self.visited_cells_by_player.items():
                        for cell in cells:
                            if cell[0] == row and cell[1] == col:
                                for player in self.game.players:
                                    if player_id == player.id:
                                        self.set_player_inactive(player)
                                        print("Player " + player.name + ", id " + str(player.id) + "collision and is "
                                                                                                   "inactive now")

    def is_game_running(self) -> bool:
        active_player_ctr = 0
        for player in self.game.players:
            if player.active:
                active_player_ctr += 1
        return active_player_ctr >= 2

    def get_and_visit_cells(self, player: Player, action: Action) -> List[Tuple[int, int]]:
        visited_cells = []

        self.change_player_status_by_action(player, action)

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

        for i in range(0, player.speed):
            visited_cells.append(
                (player.y + (i + 1) * vertical_multiplier, player.x + (i + 1) * horizontal_multiplier))

        if self.turn.turn_ctr % 6 == 0 and len(visited_cells) > 1:  # Lücke, also nur die erste und letzte Punkt nehmen
            visited_cells = [visited_cells[0], visited_cells[-1]]

        for (y, x) in visited_cells:
            if x not in range(self.game.width) or y not in range(self.game.height):
                raise PlayerOutsidePlaygroundException(player)
            player.x = visited_cells[-1][1]
            player.y = visited_cells[-1][0]
            if self.game.cells[y][x].players is None:
                self.game.cells[y][x].players = [player]
            else:
                self.game.cells[y][x].players.append(player)

        return visited_cells

    def change_player_status_by_action(self, player: Player, action: Action):
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

        if player.speed not in range(0, 11):
            raise PlayerSpeedNotInRangeException(player)

    def set_player_inactive(self, player: Player):
        if player in self.turn.playersWithPendingAction:
            self.turn.playersWithPendingAction.remove(player)
        player.active = False
