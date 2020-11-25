from contextlib import closing
from datetime import datetime, timedelta, timezone
from random import randint
import sqlite3

from chillow.controller import OfflineController
from chillow.model.cell import Cell
from chillow.model.direction import Direction
from chillow.model.game import Game
from chillow.model.player import Player
from chillow.service.ai import *
from chillow.service.ai.artificial_intelligence import ArtificialIntelligence
from chillow.view.headless_view import HeadlessView


class AIEvaluationController(OfflineController):

    def __init__(self, runs: int, db_path: str):
        super().__init__(HeadlessView())
        self.__runs = runs
        self.__db_path = db_path
        self.__connection = None
        self.__cursor = None

    def play(self):
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
        height = randint(30, 70)
        width = randint(30, 70)

        player_count = randint(3, 6)
        players = []
        for i in range(player_count):
            player = Player(i, randint(0, width - 1), randint(0, height - 1), Direction.get_random_direction(), 1, True,
                            str(i))
            players.append(player)

        cells = [[Cell() for _ in range(width)] for _ in range(height)]
        for player in players:
            cells[player.y][player.x] = Cell([player])

        self._game = Game(width, height, cells, players, 1, True, datetime.now() + timedelta(5, 15))

        self._ais = []

        self._ais.append(PathfindingAI(players[0], randint(1, 3), randint(1, 3) * 25))
        self._ais.append(PathfindingSearchTreeAI(players[1], randint(1, 3), randint(1, 3) * 25, randint(2, 4), 0.75,
                                                 randint(1, 3) * 10))
        self._ais.append(SearchTreePathfindingAI(players[2], randint(1, 3), randint(1, 3) * 25, randint(2, 4),
                                                 randint(1, 3) * 10))
        if player_count > 3:
            self._ais.append(SearchTreeAI(players[3], randint(1, 3), randint(2, 4), True, randint(1, 3) * 10))
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

                # Save how often an AI configuration participated in a game
                self.__cursor.execute("INSERT INTO participants VALUES ({}, {}, '{}', '{}')"
                                      .format(ai.player.id, self.__current_game_id, ai_class, ai_info))

                # Save how often an AI configuration won a game
                if ai.player == winner_player:
                    self.__cursor.execute("INSERT INTO winners VALUES ({}, {})"
                                          .format(ai.player.id, self.__current_game_id))

            self.__connection.commit()

    def __create_db_tables(self):
        self.__cursor.execute("CREATE TABLE IF NOT EXISTS games (id INTEGER, width INTEGER, height INTEGER, date TEXT)")
        self.__cursor.execute("CREATE TABLE IF NOT EXISTS participants (id INTEGER, game_id INTEGER, class TEXT,"
                              "info TEXT)")
        self.__cursor.execute("CREATE TABLE IF NOT EXISTS winners (id INTEGER, game_id INTEGER)")
        self.__cursor.execute("CREATE TABLE IF NOT EXISTS execution_times (player_id INTEGER, game_id INTEGER,"
                              "execution REAL)")

    def _log_execution_time(self, ai: ArtificialIntelligence, execution_time: float):
        self.__cursor.execute("INSERT INTO execution_times VALUES ({}, {}, {})"
                              .format(ai.player.id, self.__current_game_id, execution_time))
