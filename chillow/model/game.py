from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from chillow.model.player import Player
from chillow.model.cell import Cell


@dataclass
class Game:

    width: int
    height: int
    cells: List[List[Cell]]
    players: List[Player]
    you: str
    running: bool
    deadline: datetime
    _you: Player = None

    def __post_init__(self):
        if len(self.cells) != self.height:
            raise AttributeError("Cell array does not fit to game height")

        if len(self.cells[0]) != self.width:
            raise AttributeError("Cell array does not fit to game width")

        for player in self.players:
            if str(player.id) == self.you:
                self._you = player
                break

        if self._you is None:
            raise AttributeError("Your own player was not found in the game")
