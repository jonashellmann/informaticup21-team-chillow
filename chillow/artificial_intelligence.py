import random

from abc import ABCMeta, abstractmethod

from chillow.model.action import Action
from chillow.model.game import Game
from chillow.model.player import Player


class ArtificialIntelligence(metaclass=ABCMeta):

    def __init__(self, player: Player):
        self.player = player

    @abstractmethod
    def create_next_action(self, game: Game) -> Action:
        raise NotImplementedError


class ChillowAI(ArtificialIntelligence):

    def create_next_action(self, game: Game) -> Action:
        # Todo: Implement
        return Action.change_nothing
        # return random.choice(list(Action))
