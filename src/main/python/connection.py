import os
import websockets

from abc import ABCMeta, abstractmethod

from .data_loader import JSONDataLoader
from .data_writer import JSONDataWriter
from .artificial_intelligence import ChillowAI


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

    async def play(self):
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
        pass
