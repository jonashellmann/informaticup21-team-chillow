import asyncio
import os
import time
from datetime import datetime
import websockets

from abc import ABCMeta, abstractmethod

from chillow.data_loader import JSONDataLoader
from chillow.data_writer import JSONDataWriter
from chillow.artificial_intelligence import ChillowAI
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
        self.ai = ChillowAI()

    def play(self):
        asyncio.get_event_loop().run_until_complete(self._play())

    async def _play(self):
        async with websockets.connect(f"{self.url}?key={self.key}") as websocket:
            while True:
                game_data = await websocket.recv()
                game = self.data_loader.load(game_data)
                action = self.ai.create_next_action(game)
                data_out = self.data_writer.write(action)
                await websocket.send(data_out)


class OfflineConnection(Connection):

    def play(self):
        #  ToDo: Implement
        player1 = Player("1", 10, 10, Direction.down, 1, True, "Player 1")
        player2 = Player("2", 30, 30, Direction.up, 1, True, "Player 2")
        players = [player1, player2]
        field_size = 40
        cells = [[Cell() for i in range(field_size)] for j in range(field_size)]
        cells[10][10] = Cell(player1)
        cells[30][30] = Cell(player2)
        game = Game(field_size, field_size, cells, players, 1, True, datetime.now())

        if "DEACTIVATE_PYGAME" not in os.environ or not os.environ["DEACTIVATE_PYGAME"]:
            monitoring = GraphicalMonitoring(game)
        else:
            monitoring = ConsoleMonitoring()

        while True:
            monitoring.update(game)
            time.sleep(1)  # Sleep for 1 sek
