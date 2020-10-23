from dataclasses import dataclass

from model.player import Player


@dataclass
class Cell:

    player: Player = None
