from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime
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
                         or len(self.cells[player.y][player.x].players) != 1
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

    def get_other_players(self, p: Player) -> list[Player]:
        players = []
        for player in self.players:
            if player.id != p.id:
                players.append(player)
        return players

    def get_player_by_id(self, player_id: int) -> Player:
        for player in self.players:
            if player.id == player_id:
                return player
        raise PlayerWithGivenIdNotAvailableException(player_id)

    def copy(self):
        return deepcopy(self)
