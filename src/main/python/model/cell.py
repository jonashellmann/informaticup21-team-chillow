from dataclasses import dataclass

from .player import Player


@dataclass
class Cell:

    player: Player = None
