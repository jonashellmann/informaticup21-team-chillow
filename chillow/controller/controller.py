import multiprocessing
from abc import ABCMeta, abstractmethod

from chillow.model.game import Game
from chillow.service.ai.artificial_intelligence import ArtificialIntelligence
from chillow.view.view import View


class Controller(metaclass=ABCMeta):
    """Connects the services to execute the game logic and controls an UI."""

    def __init__(self, view: View):
        """Creates a new controller.

        Args:
            view: The UI that should be used.
        """
        self._view = view

    @abstractmethod
    def play(self):
        """Executes the logic to play a game and show the state in an UI."""
        pass

    @staticmethod
    def call_ai(ai: ArtificialIntelligence, game: Game, return_value: multiprocessing.Value):
        ai.create_next_action(game, return_value)
