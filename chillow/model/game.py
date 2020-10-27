from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from chillow.model.player import Player
from chillow.model.cell import Cell


@dataclass
class Game:

    width: int
    height: int
    cells: List[List[Cell]]  # First index is the row (y), second index is the column (x).
    players: List[Player]
    _you: int = field(repr=False)
    you: Player = field(init=False)
    running: bool
    deadline: datetime

    def __post_init__(self):
        if len(self.cells) != self.height:
            raise AttributeError("Cell array does not fit to game height")

        if len(self.cells[0]) != self.width:
            raise AttributeError("Cell array does not fit to game width")

        for player in self.players:
            if player.id == self._you:
                self.you = player
                break

        if self.you is None:
            raise AttributeError("Your own player was not found in the game")
