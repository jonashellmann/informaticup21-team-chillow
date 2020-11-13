from abc import ABCMeta, abstractmethod

from chillow.model.game import Game


class View(metaclass=ABCMeta):

    def __init__(self):
        self._interface_initialized = False
        self._colors = None
        self._player_colors = {0: (0, 0, 0)}

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
        assert self._colors is not None and len(self._colors) > 0, "No colors available for interface"

        self._interface_initialized = True
        for i in range(0, len(game.players)):
            self._player_colors[int(game.players[i].id)] = self._colors[i % len(self._colors)]
