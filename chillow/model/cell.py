from dataclasses import dataclass

from chillow.model.player import Player


@dataclass
class Cell:

    players: Player = None  # List of players

    def get_player_id(self) -> int:
        return 0 if self.players is None else self.players[0].id
