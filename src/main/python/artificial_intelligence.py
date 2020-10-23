import random

from abc import ABCMeta, abstractmethod

from model.action import Action
from model.game import Game


class ArtificialIntelligence(metaclass=ABCMeta):

    @abstractmethod
    def create_next_action(self, game: Game) -> Action:
        raise NotImplementedError


class ChillowAI(ArtificialIntelligence):

    def create_next_action(self, game: Game) -> Action:
        # Todo: Implement
        return random.choice(list(Action))
