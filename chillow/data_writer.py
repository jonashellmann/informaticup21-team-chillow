import json

from abc import ABCMeta, abstractmethod
from chillow.action import Action


class DataWriter(metaclass=ABCMeta):

    @abstractmethod
    def write(self, action: Action) -> str:
        raise NotImplementedError


class JSONDataWriter(DataWriter):

    def write(self, action: Action) -> str:
        return json.dumps({"action": action.name})
