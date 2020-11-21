from datetime import datetime, timedelta, timezone
from multiprocessing import Value
from random import randint

from chillow.controller.controller import Controller
from chillow.model.action import Action
from chillow.model.cell import Cell
from chillow.model.direction import Direction
from chillow.model.game import Game
from chillow.model.player import Player
from chillow.service.ai import *
from chillow.service.game_service import GameService
from chillow.view.view import View


class OfflineController(Controller):

    def __init__(self, monitoring: View):
        super().__init__(monitoring)

    def play(self):
        self._create_game()
        game_service = GameService(self._game)

        self.monitoring.update(self._game)

        while self._game.running:
            self._game.deadline = datetime.now() + timedelta(0, randint(5, 15))

            for ai in self._ais:
                if ai.player.active:
                    value = Value('i')
                    ai.create_next_action(self._game.copy(), value)
                    game_service.do_action(ai.player, Action.get_by_index(value.value))
                    self._game.deadline = datetime.now(timezone.utc) + timedelta(0, randint(5, 15))

            # if player1.active:
            #     action = self.monitoring.read_next_action()
            #     game_service.do_action(player1, action)

            self.monitoring.update(self._game)

    def _create_game(self) -> None:
        player1 = Player(1, 5, 5, Direction.down, 1, True, "Human Player 1")
        player2 = Player(2, 25, 5, Direction.down, 1, True, "AI Player 1")
        player3 = Player(3, 5, 15, Direction.up, 1, True, "AI Player 2")
        player4 = Player(4, 25, 15, Direction.up, 1, True, "AI Player 4")
        players = [player1, player2, player3, player4]
        height = 20
        width = 30
        cells = [[Cell() for _ in range(width)] for _ in range(height)]
        cells[player1.y][player1.x] = Cell([player1])
        cells[player2.y][player2.x] = Cell([player2])
        cells[player3.y][player3.x] = Cell([player3])
        cells[player4.y][player4.x] = Cell([player4])

        self._game = Game(width, height, cells, players, 1, True, datetime.now())

        ai0 = PathfindingAI(player1, 2, 75)
        ai1 = NotKillingItselfAI(player2, [AIOptions.max_distance], 1, 0)
        ai2 = SearchTreePathfindingAI(player3, 2, 75, 2)
        ai3 = SearchTreeAI(player4, 2)

        self._ais = [ai0, ai1, ai2, ai3]
