import json
import iso8601

from datetime import datetime, timedelta
from abc import ABCMeta, abstractmethod

from chillow.model.direction import Direction
from chillow.model.game import Game
from chillow.model.player import Player
from chillow.model.cell import Cell


class DataLoader(metaclass=ABCMeta):
    """Class used to convert a string to a python object"""

    @abstractmethod
    def load(self, game_data: str) -> Game:
        """Converts a string to a game.

        Args:
            game_data: The string containing the game data.

        Returns:
            The game created based on the information from the string.
        """
        pass

    @abstractmethod
    def read_server_time(self, time_data: str) -> datetime:
        """Parses a string to a Python datetime.

        Args:
            time_data: The string containing the time data.

        Returns:
            The Python datetime created based on the information from the string.
        """
        pass


class JSONDataLoader(DataLoader):
    """Class used to convert a JSON string to a python object."""

    def load(self, game_data: str) -> Game:
        """See base class."""
        json_data = json.loads(game_data)
        players = []
        cells = []

        for json_player in json_data["players"]:
            player = Player(
                int(json_player),
                int(json_data["players"][json_player]["x"]),
                int(json_data["players"][json_player]["y"]),
                Direction[json_data["players"][json_player]["direction"]],
                int(json_data["players"][json_player]["speed"]),
                json_data["players"][json_player]["active"],
                json_data["players"][json_player]["name"] if "name" in json_data["players"][json_player] else ""
            )
            players.append(player)

        for json_row in json_data["cells"]:
            row = []
            for json_cell in json_row:
                cell = Cell()
                if json_cell != 0:
                    if json_cell == -1:
                        # If there is a collision cell, it is not defined by which players this cell is occupied.
                        # Therefore is it always filled with the first player so the cell is not empty.
                        cell = Cell([players[0]])
                    else:
                        for player in players:
                            if player.id == json_cell:
                                cell = Cell([player])
                row.append(cell)
            cells.append(row)

        return Game(
            int(json_data["width"]),
            int(json_data["height"]),
            cells,
            players,
            int(json_data["you"]),
            json_data["running"],
            iso8601.parse_date(json_data["deadline"]) if json_data["running"] else None
        )

    def read_server_time(self, time_data: str) -> datetime:
        """See base class."""
        json_data = json.loads(time_data)
        return iso8601.parse_date(json_data["time"]) + timedelta(milliseconds=int(json_data["milliseconds"]))
