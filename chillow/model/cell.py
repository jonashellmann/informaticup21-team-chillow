from dataclasses import dataclass
from typing import List

from chillow.model.player import Player


@dataclass
class Cell:

    players: List[Player] = None  # List of players

    def get_player_id(self) -> int:
        return 0 if self.players is None or len(self.players) == 0 else self.players[0].id
