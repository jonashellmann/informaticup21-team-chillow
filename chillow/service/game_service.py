import logging
from typing import List, Tuple
from datetime import datetime, timedelta

import chillow.exceptions as ex
from chillow.exceptions import InvalidPlayerMoveException, PlayerSpeedNotInRangeException
from chillow.model.game import Game
from chillow.model.action import Action
from chillow.model.player import Player
from chillow.model.direction import Direction


class GameService:
    """Class that manipulates a game object by performing the actions of players."""

    def __init__(self, game: Game, ignore_deadline: bool = True):
        """ Constructor that initializes the necessary attributes.

        It also creates a turn object that represents the play moves.

        Args:
            game: The game object in which the AI is located and contains the current status of the game.
            ignore_deadline: Flag to ignore the deadline.
        """
        self.game = game
        self.turn = Turn(self.game.players, game.deadline)
        self.visited_cells_by_player = {}
        self.__ignore_deadline = ignore_deadline

    def do_action(self, player: Player, action: Action):
        """ Performs the action for a player and checks if the game is finished and which players have died when a
        new turn starts.

        Args:
            player: The player who wants to perform the action.
            action: The action to perform.
        Raises:
            InvalidPlayerMoveException:
                The player is outside the field, has reached an invalid player speed or was not
                allowed to take any further action this turn.
        """
        try:
            new_turn = self.turn.action(player)
            action_to_perform = action \
                if self.__ignore_deadline or datetime.now(self.game.deadline.tzinfo) <= self.game.deadline \
                else Action.get_default()
            self.visited_cells_by_player[player.id] = self.get_and_visit_cells(player, action_to_perform)

            if new_turn:
                self.check_and_set_died_players()

        except InvalidPlayerMoveException:
            self.set_player_inactive(player)

        self.game.running = self.is_game_running()

    def check_and_set_died_players(self):
        """Checks which players have died this turn and sets them to inactive. """
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
        """ Checks if the game is still running.

        Returns:
            True if the game is still running otherwise False.
        """
        active_player_ctr = 0
        for player in self.game.players:
            if player.active:
                active_player_ctr += 1
        return active_player_ctr >= 2

    @staticmethod
    def get_horizontal_and_vertical_multiplier(player: Player) -> Tuple[int, int]:
        """ Calculates a vertical and horizontal multiplier that can be used to calculate player movement.

        Args:
            player: The player whose movement is calculated.

        Returns:
            Horizontal and vertical multiplier.
        """
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
        """ Simulation of a player performing an action.

        Args:
            player: The player who performs the action.
            action: The Action to perform.

        Returns:
            List of field coordinates that the player has visited.
        """
        visited_cells = []
        GameService.change_player_status_by_action(player, action)
        horizontal_multiplier, vertical_multiplier = GameService.get_horizontal_and_vertical_multiplier(player)

        for i in range(1, player.speed + 1):
            visited_cells.append((player.x + i * horizontal_multiplier, player.y + i * vertical_multiplier))

        if self.turn.turn_ctr % 6 == 0 and len(visited_cells) > 1:  # Lücke, also nur ersten und letzten Punkt nehmen
            visited_cells = [visited_cells[0], visited_cells[-1]]

        visited_cells_result = []
        for (x, y) in visited_cells:
            if x not in range(self.game.width) or y not in range(self.game.height):
                self.set_player_inactive(player)
                break
            player.x = x
            player.y = y
            visited_cells_result.append((x, y))
            if self.game.cells[y][x].players is None or len(self.game.cells[y][x].players) == 0:
                self.game.cells[y][x].players = [player]
            else:
                self.game.cells[y][x].players.append(player)

        return visited_cells_result

    @staticmethod
    def change_player_status_by_action(player: Player, action: Action):
        """ Changes the direction of the player based on the action.

        Args:
            player: The player whose direction is to be changed.
            action: The Action to perform.
        """
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
        """ Sets a player inactive.

        Args:
            player: The player to be set inactive.
        """
        if player in self.turn.playersWithPendingAction:
            self.turn.playersWithPendingAction.remove(player)
        player.active = False


class Turn:
    """Class that represents a game turn."""

    def __init__(self, players: List[Player], deadline):
        """ Constructor that initializes the necessary attributes.

        Args:
            players: List of players that are in the game.
            deadline: Deadline of the game turn.
        """
        self.players = players.copy()
        self.playersWithPendingAction = players.copy()
        self.deadline = deadline
        self.turn_ctr = 1

    def action(self, player):
        """ Checks if the player is allowed to take an action and if so, removes him from the list of players who must
        take an action this turn.

        In addition a new turn is started when all players have taken an action.

        Args:
            player: Player who wants to perform an action this turn.

        Returns:
            True if the Turn is ended otherwise False.

        Raises:
            MultipleActionByPlayerException: Raised if the player did more than one action this turn.
        """
        if player not in self.playersWithPendingAction:
            raise ex.MultipleActionByPlayerException(player)
        # elif self.deadline < datetime.now():
        #    raise ex.DeadLineExceededException(player)
        else:
            self.playersWithPendingAction.remove(player)
            if len(self.playersWithPendingAction) == 0:
                self.turn_ctr += 1
                self.deadline = datetime.now() + timedelta(0, 180)
                for player in self.players:
                    if player.active:
                        self.playersWithPendingAction.append(player)
                return True  # Turn ended
            return False  # Turn not ended
