from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.best_first import BestFirst

from chillow.model.player import Player
from chillow.model.cell import Cell
from chillow.exceptions import WrongGameWidthException, WrongGameHeightException, OwnPlayerMissingException, \
    PlayerPositionException, PlayerWithGivenIdNotAvailableException


@dataclass
class Game:
    """This class holds all information needed to represent the current state of a game.

    Attributes:
        width: The number of horizontally adjacent cells.
        height: The number of vertically adjacent cells.
        cells:
            A two-dimensional list of cells.
            The first dimension is the row number (y axis), the second dimension represents the column (x axis).
            The field [0][0] is in the upper left corner.
        players: All players participating in this game.
        you: The own player in this game. This player is also part of the players list.
        running: This flag indicates whether the game is still running or is ended.
        deadline:
            The deadline by which all players have to perform their next action.
            This field has no value, if the game is not running.
    """

    width: int
    height: int
    cells: List[List[Cell]]
    players: List[Player]
    __you: int = field(repr=False)
    you: Player = field(init=False)
    running: bool
    deadline: datetime = None

    def __post_init__(self):
        """Performs checks after the game was created.

        Raises:
            WrongGameHeightException: Game height and height of cell array are not the same.
            WrongGameWidthException: Game width and width of cell array are not the same.
            PlayerPositionException: The current position of the player is not represented in the game.
            OwnPlayerMissingException: No player representing the own player was found in the game.
        """
        if len(self.cells) != self.height:
            raise WrongGameHeightException(len(self.cells), self.height)

        if len(self.cells[0]) != self.width:
            raise WrongGameWidthException(len(self.cells[0]), self.width)

        for player in self.players:
            if player.id == self.__you:
                self.you = player

            if player.active \
                    and (self.cells[player.y][player.x].players is None
                         or player not in self.cells[player.y][player.x].players):
                raise PlayerPositionException(player.x, player.y)

        if not hasattr(self, 'you'):
            raise OwnPlayerMissingException()

    def get_winner(self) -> Optional[Player]:
        """Returns the winner of the game.

        The winner is only determined if the game is not running anymore and there is an active player left in the
        game. Otherwise an empty value is returned.

        Returns:
            The winner of the game if there is one. The return vale may be empty.
        """
        if self.running:
            raise Exception("Game not ended and has no winner yet")
        for player in self.players:
            if player.active:
                return player
        return None

    def get_other_player_ids(self, p: Player, distance: int = 0, check_active: bool = False) -> List[int]:
        """Returns all other players in the game reachable in given distance and based on their status.

        Args:
            p: The player who should be ignored.
            distance: The distance in which other players should be found; 0 if distance should be ignored.
            check_active: Flag to check whether only active players should be returned.

        Returns:
            List of ids matching the above criteria.
        """
        players = []
        for player in self.players:
            if player.id != p.id \
                    and (not check_active or player.active) \
                    and (distance == 0 or (0 < self.__measure_shortest_distance(player, p) <= distance)):
                players.append(player.id)
        return players

    def __measure_shortest_distance(self, player_a: Player, player_b: Player) -> int:
        matrix = self.translate_cell_matrix_to_pathfinding_matrix()
        matrix[player_b.y][player_b.x] = 1  # target field must be empty
        path_finder = BestFirst(diagonal_movement=DiagonalMovement.never)
        grid = Grid(matrix=matrix)

        path, _ = path_finder.find_path(grid.node(player_a.x, player_a.y), grid.node(player_b.x, player_b.y), grid)
        return len(path) - 1  # Subtract 1 to not count the starting position

    def translate_cell_matrix_to_pathfinding_matrix(self) -> List[List[int]]:
        """Translates the two-dimensional cell array to an two-dimensional array usable for pathfinding.

        Returns:
            Two-dimensional array of integers, where an empty cell is represented by 1 and cells which were already
            visited by a player are represented by 0.
        """
        matrix = [[1 for _ in range(self.width)] for _ in range(self.height)]
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                if self.cells[i][j].players is not None and len(self.cells[i][j].players) > 0:
                    matrix[i][j] = 0  # Collision cell
        return matrix

    def get_player_by_id(self, player_id: int) -> Player:
        """Identifies one player in the game by the ID.

        Args:
            player_id: The ID of the player.

        Returns:
            The player identified by the given ID.

        Raises:
             PlayerWithGivenIdNotAvailableException: Raised when no player with this ID is in this game.
        """
        for player in self.players:
            if player.id == player_id:
                return player
        raise PlayerWithGivenIdNotAvailableException(player_id)

    def get_players_by_ids(self, player_ids: List[int]) -> List[Player]:
        """Identifies multiple players in the game by their IDs.

        Args:
            player_ids: A list of IDs of the players.

        Returns:
            A list of players identified by the given IDs.
        """
        players = []
        for player in self.players:
            if player.id in player_ids:
                players.append(player)
        return players

    def copy(self):
        """Creates an exact same copy of this game but all objects point to different memory locations.

        Returns:
            A copy of the game.
        """
        players: List[Player] = []
        for player in self.players:
            players.append(
                Player(player.id, player.x, player.y, player.direction, player.speed, player.active, player.name))

        cells: List[List[Cell]] = [[Cell() for _ in range(self.width)] for _ in range(self.height)]
        for row in range(len(self.cells)):
            for col in range(len(self.cells[row])):
                if self.cells[row][col].players is not None:
                    players_in_cell = []
                    for player in self.cells[row][col].players:
                        for copied_player in players:
                            if copied_player.id == player.id:
                                players_in_cell.append(copied_player)
                    cells[row][col].players = players_in_cell

        return Game(self.width, self.height, cells, players, self.you.id, self.running, self.deadline)

    def normalize_deadline(self, server_time: datetime, own_time: datetime) -> None:
        """Adjusts the deadline according to the difference between server and system time.

        Args:
            server_time: The current time of the game server.
            own_time: The current time of the system where the program is executed.
        """
        time_delta = own_time - server_time
        multiplier = 1

        if server_time > own_time:
            time_delta = server_time - own_time
            multiplier = -1

        microseconds_delta = int((time_delta.total_seconds() * 1000000))
        self.deadline += multiplier * timedelta(microseconds=microseconds_delta)
