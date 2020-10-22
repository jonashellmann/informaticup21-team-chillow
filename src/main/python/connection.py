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

    def play(self):
        async with websockets.connect(f"{self.url}?key={self.key}") as websocket:
            while True:
                data = await websocket.recv()
                data_object = self.data_loader.load(data)
                action = self.ai.create_next_action(data_object)
                data_out = self.data_writer.write(action)
                await websocket.send(data_out)


class OfflineConnection(Connection):

    def play(self):
        #  ToDo: Implement
        pass
