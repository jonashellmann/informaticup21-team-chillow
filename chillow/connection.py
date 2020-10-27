import asyncio
import os
from datetime import datetime, timedelta
import websockets

from abc import ABCMeta, abstractmethod

from chillow.data_loader import JSONDataLoader
from chillow.data_writer import JSONDataWriter
from chillow.artificial_intelligence import ChillowAI, NotKillingItselfAI
from chillow.game_services.game_service import GameService
from chillow.monitoring import GraphicalMonitoring, ConsoleMonitoring
from chillow.model.game import Game
from chillow.model.player import Player
from chillow.model.direction import Direction
from chillow.model.cell import Cell


class Connection(metaclass=ABCMeta):

    @abstractmethod
    def play(self):
        raise NotImplementedError


class OnlineConnection(Connection):

    def __init__(self):
        self.url = os.environ["URL"]
        self.key = os.environ["KEY"]
        self.data_loader = JSONDataLoader()
        self.data_writer = JSONDataWriter()
        self.ai = None

    def play(self):
        asyncio.get_event_loop().run_until_complete(self._play())

    async def _play(self):
        async with websockets.connect(f"{self.url}?key={self.key}") as websocket:
            while True:
                game_data = await websocket.recv()
                game = self.data_loader.load(game_data)
                if self.ai is None:
                    self.ai = ChillowAI(game.you)
                action = self.ai.create_next_action(game)
                data_out = self.data_writer.write(action)
                await websocket.send(data_out)


class OfflineConnection(Connection):

    def play(self):
        player1 = Player(1, 10, 10, Direction.down, 1, True, "Human Player 1")
        player2 = Player(2, 10, 30, Direction.down, 1, True, "AI Player 1")
        player3 = Player(3, 30, 10, Direction.up, 1, True, "AI Player 2")
        player4 = Player(4, 30, 30, Direction.up, 1, True, "AI Player 4")
        players = [player1, player2, player3, player4]
        field_size = 40
        cells = [[Cell() for i in range(field_size)] for j in range(field_size)]
        cells[player1.y][player1.x] = Cell([player1])
        cells[player2.y][player2.x] = Cell([player2])
        cells[player3.y][player3.x] = Cell([player3])
        cells[player4.y][player4.x] = Cell([player4])
        game = Game(field_size, field_size, cells, players, 1, True, datetime.now() + timedelta(0, 180))

        if "DEACTIVATE_PYGAME" not in os.environ or not os.environ["DEACTIVATE_PYGAME"]:
            monitoring = GraphicalMonitoring(game)
        else:
            monitoring = ConsoleMonitoring()
        monitoring.update(game)

        game_service = GameService(game)
        ai0 = NotKillingItselfAI(player1, game, True)
        ai1 = NotKillingItselfAI(player2, game, True)
        ai2 = NotKillingItselfAI(player3, game, False)
        ai3 = NotKillingItselfAI(player4, game, False)

        while game.running:
            # action = monitoring.create_next_action()
            # game_service.do_action(player1, action)

            action = ai0.create_next_action(game)
            game_service.do_action(ai0.player, action)
            action = ai1.create_next_action(game)
            game_service.do_action(ai1.player, action)
            action = ai2.create_next_action(game)
            game_service.do_action(ai2.player, action)
            action = ai3.create_next_action(game)
            game_service.do_action(ai3.player, action)

            monitoring.update(game)

        input("Enter drücken zum verlassen ... ")
