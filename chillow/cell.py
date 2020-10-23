from dataclasses import dataclass

from chillow.player import Player


@dataclass
class Cell:

    player: Player = None
