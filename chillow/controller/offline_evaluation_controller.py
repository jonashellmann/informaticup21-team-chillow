from datetime import datetime, timedelta
from random import randint

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
        self.__participants = {}
        self.__results = {}
        self.__runs = runs

    def play(self):
        for _ in range(self.__runs):
            super().play()

            winner_player = self._game.get_winner()
            for ai in self._ais:
                ai_info = ai.get_information()

                # Save how often an AI configuration participated in a game
                if ai_info in self.__participants:
                    self.__participants[ai_info] += 1
                else:
                    self.__participants[ai_info] = 1

                # Save how often an AI configuration won a game
                if ai.player == winner_player:
                    if ai_info in self.__results:
                        self.__results[ai_info] += 1
                    else:
                        self.__results[ai_info] = 1

        print("----- Participants -----")
        print(self.__participants)
        print("------- Winners --------")
        print(self.__results)

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

        self._game = Game(width, height, cells, players, 1, True, datetime.now() + timedelta(0, 180))

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
