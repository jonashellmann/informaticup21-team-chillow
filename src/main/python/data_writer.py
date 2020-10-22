import json

from abc import ABCMeta, abstractmethod


class DataWriter(metaclass=ABCMeta):

    @abstractmethod
    def write(self, action):
        raise NotImplementedError


class JSONDataWriter(DataWriter):

    def write(self, action):
        return json.dumps({"action": action.name})
