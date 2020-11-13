from abc import ABCMeta, abstractmethod
from typing import List, Any

from chillow.model.game import Game


class View(metaclass=ABCMeta):

    def __init__(self, colors: List[Any]):
        self._interface_initialized = False
        self._player_colors = {0: (0, 0, 0)}
        self.__colors = colors

    @abstractmethod
    def update(self, game: Game):
        raise NotImplementedError

    @abstractmethod
    def create_next_action(self):
        raise NotImplementedError

    @abstractmethod
    def end(self):
        raise NotImplementedError

    def _initialize_interface(self, game: Game):
        assert self.__colors is not None and len(self.__colors) > 0, "No colors available for interface"

        self._interface_initialized = True
        for i in range(0, len(game.players)):
            self._player_colors[int(game.players[i].id)] = self.__colors[i % (len(self.__colors) - 1)]
