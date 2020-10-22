import json

from abc import ABCMeta, abstractmethod


class DataLoader(metaclass=ABCMeta):

    @abstractmethod
    def load(self, data):
        raise NotImplementedError


class JSONDataLoader(DataLoader):

    def load(self, data):
        json_data = json.loads(data)
        # Todo: Fill json data in Objects and return them
        return None
