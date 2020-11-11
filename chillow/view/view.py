from abc import ABCMeta, abstractmethod

from chillow.model.game import Game


class View(metaclass=ABCMeta):

    @abstractmethod
    def update(self, game: Game):
        raise NotImplementedError

    @abstractmethod
    def create_next_action(self):
        raise NotImplementedError

    @abstractmethod
    def end(self):
        raise NotImplementedError
