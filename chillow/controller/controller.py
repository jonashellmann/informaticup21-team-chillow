from abc import ABCMeta, abstractmethod

from chillow.view.view import View


class Controller(metaclass=ABCMeta):

    def __init__(self, view: View):
        self._view = view

    @abstractmethod
    def play(self):
        raise NotImplementedError
