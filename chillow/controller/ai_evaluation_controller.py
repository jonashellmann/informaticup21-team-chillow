from contextlib import closing
from datetime import datetime, timedelta, timezone
from random import randint
import sqlite3
from typing import List

from chillow.controller import OfflineController
from chillow.model.cell import Cell
from chillow.model.direction import Direction
from chillow.model.game import Game
from chillow.model.player import Player
from chillow.service.ai import NotKillingItselfAI, PathfindingSearchTreeAI, PathfindingAI, SearchTreeAI, \
    SearchTreePathfindingAI, RandomAI, AIOptions
from chillow.service.ai.artificial_intelligence import ArtificialIntelligence
from chillow.view.headless_view import HeadlessView

# These AIs are considered as the top 25 after 1000 simulated game in the first part of the evaluation
best_ais_configurations = [
    (PathfindingSearchTreeAI.__name__, (1, 50, 2, 0.75, 30)),
    (SearchTreePathfindingAI.__name__, (1, 25, 2, 20)),
    (PathfindingSearchTreeAI.__name__, (1, 25, 2, 0.75, 10)),
    (PathfindingSearchTreeAI.__name__, (1, 75, 3, 0.75, 10)),
    (PathfindingSearchTreeAI.__name__, (2, 75, 3, 0.75, 20)),
    (PathfindingSearchTreeAI.__name__, (1, 75, 2, 0.75, 10)),
    (PathfindingAI.__name__, (1, 50)),
    (PathfindingSearchTreeAI.__name__, (1, 25, 2, 0.75, 20)),
    (PathfindingSearchTreeAI.__name__, (2, 50, 2, 0.75, 20)),
    (PathfindingSearchTreeAI.__name__, (1, 50, 2, 0.75, 20)),
    (NotKillingItselfAI.__name__, ([AIOptions.max_distance], 1, 0, 1)),
    (NotKillingItselfAI.__name__, ([AIOptions.max_distance], 2, 0, 3)),
    (PathfindingSearchTreeAI.__name__, (1, 50, 3, 0.75, 10)),
    (PathfindingSearchTreeAI.__name__, (1, 75, 3, 0.75, 30)),
    (SearchTreePathfindingAI.__name__, (1, 75, 2, 10)),
    (PathfindingAI.__name__, (1, 75)),
    (PathfindingSearchTreeAI.__name__, (1, 75, 3, 0.75, 20)),
    (SearchTreePathfindingAI.__name__, (2, 50, 2, 20)),
    (SearchTreePathfindingAI.__name__, (1, 25, 2, 10)),
    (PathfindingSearchTreeAI.__name__, (1, 75, 2, 0.75, 20)),
    (PathfindingAI.__name__, (1, 25)),
    (PathfindingSearchTreeAI.__name__, (1, 50, 3, 0.75, 30)),
    (PathfindingSearchTreeAI.__name__, (1, 50, 3, 0.75, 20)),
    (PathfindingSearchTreeAI.__name__, (2, 75, 2, 0.75, 30)),
    (SearchTreePathfindingAI.__name__, (1, 50, 2, 10))
]


class AIEvaluationController(OfflineController):
    """Executes multiple games after each other with randomly created games and players.

    The result of every game and the execution time for each player in each round is saved in an SQLite database."""

    def __init__(self, runs: int, db_path: str, evaluation_type: int):
        """ Creates a new AI evaluation controller.

        Args:
            runs: The number of games to be simulated.
            db_path: The path of the SQLite database file.
            evaluation_type: Defines which evaluation should be performed
        """
        super().__init__(HeadlessView())
        self.__runs = runs
        self.__db_path = db_path
        if 1 <= evaluation_type <= 2:
            self.__evaluation_type = evaluation_type
        else:
            self.__evaluation_type = 1
        self.__connection = None
        self.__cursor = None
        self.__current_game_id = None

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
        height = randint(30, 70)
        width = randint(30, 70)

        player_count = randint(3, 6)
        players = []
        occupied_coordinates = []
        for i in range(1, player_count + 1):
            next_coordinate = (randint(0, width - 1), randint(0, height - 1))
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
        self._game_round = 0

        self._ais = []

        if self.__evaluation_type == 1:
            self.__generate_ais_for_first_evaluation(player_count, players)
        elif self.__evaluation_type == 2:
            self.__generate_ais_for_second_evaluation(player_count, players)

    def __generate_ais_for_first_evaluation(self, player_count: int, players: List[Player]) -> None:
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

    def __generate_ais_for_second_evaluation(self, player_count: int, players: List[Player]) -> None:
        used_ai_indices = []
        for i in range(player_count):
            ai_index = randint(0, len(best_ais_configurations) - 1)
            # Prevent that the same AI configuration is used in one game
            while ai_index in used_ai_indices:
                ai_index = randint(0, len(best_ais_configurations) - 1)

            used_ai_indices.append(ai_index)
            ai = best_ais_configurations[ai_index]
            self._ais.append(globals()[ai[0]](players[i], *ai[1]))

    def __run_simulations(self, max_game_id):
        for i in range(self.__runs):
            self.__current_game_id = i + 1 + max_game_id
            super().play()

            self.__cursor.execute("INSERT INTO games VALUES ({}, {}, {}, '{}', NULL)"
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
                    self.__cursor.execute("UPDATE games SET winner_id = {} WHERE id = {}"
                                          .format(player_id, self.__current_game_id))

            self.__connection.commit()

    def __create_db_tables(self):
        self.__cursor.execute("CREATE TABLE IF NOT EXISTS players ("
                              "id INTEGER NOT NULL PRIMARY KEY,"
                              "class TEXT NOT NULL,"
                              "info TEXT)")
        self.__cursor.execute("CREATE TABLE IF NOT EXISTS games ("
                              "id INTEGER NOT NULL PRIMARY KEY,"
                              "width INTEGER NOT NULL,"
                              "height INTEGER NOT NULL,"
                              "date TEXT NOT NULL,"
                              "winner_id INTEGER,"
                              "FOREIGN KEY (winner_id) REFERENCES players (id))")
        self.__cursor.execute("CREATE TABLE IF NOT EXISTS participants ("
                              "player_id INTEGER NOT NULL,"
                              "game_id INTEGER NOT NULL,"
                              "PRIMARY KEY(player_id, game_id),"
                              "FOREIGN KEY (player_id) REFERENCES players (id),"
                              "FOREIGN KEY (game_id) REFERENCES games (id))")
        self.__cursor.execute("CREATE TABLE IF NOT EXISTS execution_times ("
                              "player_id INTEGER NOT NULL,"
                              "game_id INTEGER NOT NULL,"
                              "game_round INTEGER NOT NULL,"
                              "execution REAL NOT NULL,"
                              "PRIMARY KEY(player_id, game_id, game_round),"
                              "FOREIGN KEY (player_id) REFERENCES players (id),"
                              "FOREIGN KEY (game_id) REFERENCES games (id))")

    def _log_execution_time(self, ai: ArtificialIntelligence, execution_time: float):
        ai_class = ai.__class__.__name__
        ai_info = ai.get_information()
        player_id = self.__get_player_id(ai_class, ai_info)

        self.__cursor.execute("INSERT INTO execution_times VALUES ({}, {}, {}, {})"
                              .format(player_id, self.__current_game_id, self._game_round, execution_time))

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
