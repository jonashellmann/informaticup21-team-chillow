from dataclasses import dataclass

from chillow.model.player import Player


@dataclass
class Cell:

    player: Player = None
