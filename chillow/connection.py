import os
import websockets
import asyncio

from abc import ABCMeta, abstractmethod

from chillow.data_loader import JSONDataLoader
from chillow.data_writer import JSONDataWriter
from chillow.artificial_intelligence import ChillowAI


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
        pass
