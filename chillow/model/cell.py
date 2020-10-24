from dataclasses import dataclass

from chillow.model.player import Player


@dataclass
class Cell:

    player: Player = None

    def get_player_id(self) -> int:
        return 0 if self.player is None else self.player.id
