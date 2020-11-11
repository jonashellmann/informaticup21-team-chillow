from abc import ABCMeta, abstractmethod

from chillow.view.view import View


class Controller(metaclass=ABCMeta):

    def __init__(self, monitoring: View):
        self.monitoring = monitoring

    @abstractmethod
    def play(self):
        raise NotImplementedError
