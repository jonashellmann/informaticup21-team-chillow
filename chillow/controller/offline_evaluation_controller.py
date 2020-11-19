from datetime import datetime, timedelta, timezone
from random import randint
import sqlite3

from chillow.controller import OfflineController
from chillow.model.cell import Cell
from chillow.model.direction import Direction
from chillow.model.game import Game
from chillow.model.player import Player
from chillow.service.ai import *
from chillow.view.headless_view import HeadlessView


class OfflineEvaluationController(OfflineController):

    def __init__(self, runs: int):
        super().__init__(HeadlessView())
        self.__runs = runs

        self.__connection = sqlite3.connect("evaluation.db")
        self.__cursor = self.__connection.cursor()
        self.__cursor.execute("CREATE TABLE IF NOT EXISTS games (id INTEGER, width INTEGER, height INTEGER, date TEXT)")
        self.__cursor.execute("CREATE TABLE IF NOT EXISTS participants (id INTEGER, game_id INTEGER, class TEXT,"
                              "info TEXT)")
        self.__cursor.execute("CREATE TABLE IF NOT EXISTS winners (id INTEGER, game_id INTEGER)")

    def play(self):
        max_game_id = self.__cursor.execute("SELECT MAX(id) FROM games").fetchone()[0]
        if max_game_id is None:
            max_game_id = 0

        for i in range(self.__runs):
            super().play()

            game_id = i + 1 + max_game_id
            self.__cursor.execute("INSERT INTO games VALUES ({}, {}, {}, '{}')"
                                  .format(game_id, self._game.width, self._game.height, datetime.now(timezone.utc)))

            winner_player = self._game.get_winner()
            for ai in self._ais:
                ai_class = ai.__class__.__name__
                ai_info = ai.get_information()

                # Save how often an AI configuration participated in a game
                self.__cursor.execute("INSERT INTO participants VALUES ({}, {}, '{}', '{}')"
                                      .format(ai.player.id, game_id, ai_class, ai_info))

                # Save how often an AI configuration won a game
                if ai.player == winner_player:
                    self.__cursor.execute("INSERT INTO winners VALUES ({}, {})".format(ai.player.id, game_id))

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

        self._ais.append(PathfindingAI(players[0], randint(1, 3), randint(1, 3) * 5 + 70))
        self._ais.append(PathfindingSearchTreeAI(players[1], randint(1, 3), randint(1, 3) * 5 + 70, randint(2, 4), 0.75,
                                                 randint(1, 3) * 10))
        self._ais.append(SearchTreePathfindingAI(players[2], randint(1, 3), randint(1, 3) * 5 + 70, randint(2, 4),
                                                 randint(1, 3) * 10))
        if player_count > 3:
            self._ais.append(SearchTreeAI(players[3], randint(1, 3), randint(2, 4), True, randint(1, 3) * 10))
            if player_count > 4:
                self._ais.append(NotKillingItselfAI(players[4], [AIOptions.max_distance], randint(1, 3), 0))
                if player_count > 5:
                    self._ais.append(RandomAI(players[5], randint(1, 3)))
