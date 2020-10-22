import json

from abc import ABCMeta, abstractmethod
from src.main.python.model.game import Game


class DataLoader(metaclass=ABCMeta):

    @abstractmethod
    def load(self, data: str) -> Game:
        raise NotImplementedError


class JSONDataLoader(DataLoader):

    def load(self, game_data: str) -> Game:
        json_data = json.loads(game_data)
        # Todo: Fill json data in Objects and return them
        return None
