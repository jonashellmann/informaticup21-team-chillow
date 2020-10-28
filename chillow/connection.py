import asyncio
import os
from datetime import datetime, timedelta
import websockets

from abc import ABCMeta, abstractmethod

from chillow.service.data_loader import JSONDataLoader
from chillow.service.data_writer import JSONDataWriter
from chillow.ai.random_ai import RandomAI, RandomWaitingAI
from chillow.service.game_service import GameService
from chillow.controller.monitoring import GraphicalMonitoring, ConsoleMonitoring
from chillow.model.game import Game
from chillow.model.player import Player
from chillow.model.direction import Direction
from chillow.model.cell import Cell


class Connection(metaclass=ABCMeta):

    def __init__(self):
        if not os.getenv("DEACTIVATE_PYGAME", False):
            self.monitoring = GraphicalMonitoring()
        else:
            self.monitoring = ConsoleMonitoring()

    @abstractmethod
    def play(self):
        raise NotImplementedError


class OnlineConnection(Connection):

    def __init__(self):
        super().__init__()
        self.url = os.environ["URL"]
        self.key = os.environ["KEY"]
        self.data_loader = JSONDataLoader()
        self.data_writer = JSONDataWriter()
        self.ai = None

    def play(self):
        asyncio.get_event_loop().run_until_complete(self._play())
        self.monitoring.end()

    async def _play(self):
        async with websockets.connect(f"{self.url}?key={self.key}") as websocket:
            while True:
                game_data = await websocket.recv()
                game = self.data_loader.load(game_data)
                self.monitoring.update(game)

                if self.ai is None:
                    self.ai = RandomWaitingAI(game.you)

                if game.you.active:
                    action = self.ai.create_next_action(game)
                    data_out = self.data_writer.write(action)
                    await websocket.send(data_out)


class OfflineConnection(Connection):

    def __init__(self):
        super().__init__()

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

        self.monitoring.update(game)

        game_service = GameService(game)
        ai1 = RandomAI(player2)
        ai2 = RandomAI(player3)
        ai3 = RandomAI(player4)
        ais = [ai1, ai2, ai3]

        while game.running:
            if player1.active:
                action = self.monitoring.create_next_action()
                game_service.do_action(player1, action)

            for ai in ais:
                if ai.player.active:
                    action = ai.create_next_action(game)
                    game_service.do_action(ai.player, action)

            self.monitoring.update(game)
