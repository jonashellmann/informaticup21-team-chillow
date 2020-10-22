from dataclasses import dataclass
from datetime import datetime

from .player import Player
from .cell import Cell


@dataclass
class Game:

    width: int
    height: int
    cells: list[list[Cell]]
    players: list[Player]
    running: bool
    deadline: datetime

    def __post_init__(self):
        if len(self.cells) != self.height:
            raise AttributeError("Cell array does not fit to game height")

        if len(self.cells[0]) != self.width:
            raise AttributeError("Cell array does not fit to game width")
