from dataclasses import dataclass
from typing import List

from chillow.model.player import Player


@dataclass
class Cell:
    """This class is used to represent a cell in a game which contains none, one or multiple players.

    Attributes:
        players(List[Player]): A list of the players that have visited this cell during a game.
    """

    players: List[Player] = None  # List of players

    def get_player_id(self) -> int:
        """Gets the id of the first player who visited this cell.

        Returns:
            Returns the ID of the first player who visited this cell.
            If no player visited this cell yet, the return value is 0.
        """

        return 0 if self.players is None or len(self.players) == 0 else self.players[0].id
