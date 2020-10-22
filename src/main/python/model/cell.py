from dataclasses import dataclass, field

from .player import Player
from .game import Game


@dataclass
class Cell:

    x: int
    y: int
    game: Game
    player: Player = field(init=False)
    _player: Player = field(init=False, repr=False)

    @property
    def player(self) -> Player:
        return self._player

    @player.setter
    def player(self, player: Player):
        if self.game.has_player(player):
            self._player = player
