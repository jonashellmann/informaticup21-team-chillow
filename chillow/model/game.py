from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List

from chillow.model.player import Player
from chillow.model.cell import Cell
from chillow.exceptions import WrongGameWidthException, WrongGameHeightException, OwnPlayerMissingException, \
    PlayerPositionException, PlayerWithGivenIdNotAvailableException


@dataclass
class Game:
    width: int
    height: int
    cells: List[List[Cell]]  # First index is the row (y), second index is the column (x).
    players: List[Player]
    _you: int = field(repr=False)
    you: Player = field(init=False)
    running: bool
    deadline: datetime = None

    def __post_init__(self):
        if len(self.cells) != self.height:
            raise WrongGameHeightException(len(self.cells), self.height)

        if len(self.cells[0]) != self.width:
            raise WrongGameWidthException(len(self.cells[0]), self.width)

        for player in self.players:
            if player.id == self._you:
                self.you = player

            if player.active \
                    and (self.cells[player.y][player.x].players is None
                         or self.cells[player.y][player.x].players[0] != player):
                raise PlayerPositionException(player.x, player.y)

        if not hasattr(self, 'you'):
            raise OwnPlayerMissingException()

    def get_winner(self) -> Player:
        if self.running:
            raise Exception("Game not ended and has no winner yet")
        for player in self.players:
            if player.active:
                return player
        raise Exception("No winner in ended game found")

    def get_other_player_ids(self, p: Player, distance: int = 0) -> List[int]:
        players = []
        for player in self.players:
            if player.id != p.id and (distance == 0 or self.__measure_shortest_distance(player, p) <= distance):
                players.append(player.id)
        return players

    def __measure_shortest_distance(self, player_a: Player, player_b: Player) -> int:
        return 0

    def translate_cell_matrix_to_pathfinding_matrix(self) -> List[List[int]]:
        matrix = [[1 for _ in range(self.width)] for _ in range(self.height)]
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                if self.cells[i][j].players is not None and len(self.cells[i][j].players) > 0:
                    matrix[i][j] = 0  # Collision cell
        return matrix

    def get_player_by_id(self, player_id: int) -> Player:
        for player in self.players:
            if player.id == player_id:
                return player
        raise PlayerWithGivenIdNotAvailableException(player_id)

    def get_players_by_ids(self, player_ids: List[int]) -> List[Player]:
        players = []
        for player in self.players:
            if player.id in player_ids:
                players.append(player)
        return players

    def copy(self):
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
        seconds_delta = (server_time - own_time).total_seconds() + 3
        self.deadline -= timedelta(seconds=seconds_delta)
