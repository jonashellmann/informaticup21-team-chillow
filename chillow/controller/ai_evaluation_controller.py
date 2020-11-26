from contextlib import closing
from datetime import datetime, timedelta, timezone
from random import randint
import sqlite3
from typing import List, Tuple

from chillow.controller import OfflineController
from chillow.model.cell import Cell
from chillow.model.direction import Direction
from chillow.model.game import Game
from chillow.model.player import Player
from chillow.service.ai import *
from chillow.service.ai.artificial_intelligence import ArtificialIntelligence
from chillow.view.headless_view import HeadlessView


class AIEvaluationController(OfflineController):
    """Executes multiple games after each other with randomly created games and players.

    The result of every game and the execution time for each player in each round is saved in an SQLite database."""

    def __init__(self, runs: int, db_path: str):
        """ Creates a new AI evaluation controller.

        Args:
            runs: The number of games to be simulated.
            db_path: The path of the SQLite database file.
        """
        super().__init__(HeadlessView())
        self.__runs = runs
        self.__db_path = db_path
        self.__connection = None
        self.__cursor = None

    def play(self):
        """See base class."""
        with closing(sqlite3.connect(self.__db_path)) as connection:
            with closing(connection.cursor()) as cursor:
                self.__connection = connection
                self.__cursor = cursor

                self.__create_db_tables()

                max_game_id = self.__cursor.execute("SELECT MAX(id) FROM games").fetchone()[0]
                if max_game_id is None:
                    max_game_id = 0

                self.__run_simulations(max_game_id)

    def _create_game(self) -> None:
        height = randint(2, 2)
        width = randint(5, 5)

        player_count = randint(3, 6)
        players = []
        occupied_coordinates: List[Tuple[int, int]] = [(-1, -1)]
        for i in range(1, player_count + 1):
            next_coordinate = (-1, -1)
            while next_coordinate in occupied_coordinates:
                next_coordinate = (randint(0, width - 1), randint(0, height - 1))
            occupied_coordinates.append(next_coordinate)
            player = Player(i, next_coordinate[0], next_coordinate[1], Direction.get_random_direction(), 1, True,
                            str(i))
            players.append(player)

        cells = [[Cell() for _ in range(width)] for _ in range(height)]
        for player in players:
            cells[player.y][player.x] = Cell([player])

        self._game = Game(width, height, cells, players, 1, True, datetime.now() + timedelta(5, 15))

        self._ais = []

        self._ais.append(PathfindingAI(players[0], randint(1, 3), randint(1, 3) * 25))
        self._ais.append(PathfindingSearchTreeAI(players[1], randint(1, 3), randint(1, 3) * 25, randint(2, 3), 0.75,
                                                 randint(1, 3) * 10))
        self._ais.append(SearchTreePathfindingAI(players[2], randint(1, 3), randint(1, 3) * 25, 2,
                                                 randint(1, 3) * 10))
        if player_count > 3:
            self._ais.append(SearchTreeAI(players[3], randint(1, 3), randint(2, 3), True, randint(1, 3) * 10))
            if player_count > 4:
                self._ais.append(NotKillingItselfAI(players[4], [AIOptions.max_distance], randint(1, 3), 0,
                                                    randint(1, 3)))
                if player_count > 5:
                    self._ais.append(RandomAI(players[5], randint(1, 3)))

    def __run_simulations(self, max_game_id):
        for i in range(self.__runs):
            self.__current_game_id = i + 1 + max_game_id
            super().play()

            self.__cursor.execute("INSERT INTO games VALUES ({}, {}, {}, '{}')"
                                  .format(self.__current_game_id, self._game.width, self._game.height,
                                          datetime.now(timezone.utc)))

            winner_player = self._game.get_winner()
            for ai in self._ais:
                ai_class = ai.__class__.__name__
                ai_info = ai.get_information()
                player_id = self.__get_player_id(ai_class, ai_info)

                # Save how often an AI configuration participated in a game
                self.__cursor.execute("INSERT INTO participants VALUES ({}, {})"
                                      .format(player_id, self.__current_game_id))

                # Save how often an AI configuration won a game
                if ai.player == winner_player:
                    self.__cursor.execute("INSERT INTO winners VALUES ({}, {})"
                                          .format(player_id, self.__current_game_id))

            self.__connection.commit()

    def __create_db_tables(self):
        self.__cursor.execute("CREATE TABLE IF NOT EXISTS games (id INTEGER, width INTEGER, height INTEGER, date TEXT)")
        self.__cursor.execute("CREATE TABLE IF NOT EXISTS players (id INTEGER, class TEXT, info TEXT)")
        self.__cursor.execute("CREATE TABLE IF NOT EXISTS participants (player_id INTEGER, game_id INTEGER)")
        self.__cursor.execute("CREATE TABLE IF NOT EXISTS winners (player_id INTEGER, game_id INTEGER)")
        self.__cursor.execute("CREATE TABLE IF NOT EXISTS execution_times (player_id INTEGER, game_id INTEGER,"
                              "execution REAL)")

    def _log_execution_time(self, ai: ArtificialIntelligence, execution_time: float):
        ai_class = ai.__class__.__name__
        ai_info = ai.get_information()
        player_id = self.__get_player_id(ai_class, ai_info)

        self.__cursor.execute("INSERT INTO execution_times VALUES ({}, {}, {})"
                              .format(player_id, self.__current_game_id, execution_time))

    def __get_player_id(self, ai_class: str, ai_info: str) -> int:
        player_id = self.__cursor.execute(
            "SELECT MAX(id) FROM players p WHERE p.class = '{}' AND p.info = '{}'"
            .format(ai_class, ai_info)).fetchone()[0]

        if player_id is None:
            max_player_id = self.__cursor.execute("SELECT MAX(id) FROM players").fetchone()[0]
            if max_player_id is None:
                max_player_id = 0
            player_id = max_player_id + 1
            self.__cursor.execute("INSERT INTO players VALUES ({}, '{}', '{}')".format(player_id, ai_class, ai_info))

        return player_id
