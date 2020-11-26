import multiprocessing
from abc import ABCMeta, abstractmethod

from chillow.model.game import Game
from chillow.service.ai.artificial_intelligence import ArtificialIntelligence
from chillow.view.view import View


class Controller(metaclass=ABCMeta):

    def __init__(self, view: View):
        self._view = view

    @abstractmethod
    def play(self):
        raise NotImplementedError

    @staticmethod
    def call_ai(ai: ArtificialIntelligence, game: Game, return_value: multiprocessing.Value):
        ai.create_next_action(game, return_value)
