from datetime import datetime, timedelta

from chillow.controller.controller import Controller
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
        game = Game(width, height, cells, players, 1, True, datetime.now() + timedelta(0, 180))

        self.monitoring.update(game)

        game_service = GameService(game)
        ai0 = PathfindingAI(player1, 2, 75)
        ai1 = NotKillingItselfAI(player2, game, [AIOptions.max_distance], 1, 0)
        ai2 = SearchTreePathfindingAI(player3, 2, 75, 2)
        ai3 = SearchTreeAI(player4, 2)
        ais = [ai0, ai1, ai2, ai3]

        while game.running:
            # if player1.active:
            #     action = self.monitoring.create_next_action()
            #     game_service.do_action(player1, action)

            for ai in ais:
                if ai.player.active:
                    action = ai.create_next_action(game.copy())
                    game_service.do_action(ai.player, action)

            self.monitoring.update(game)