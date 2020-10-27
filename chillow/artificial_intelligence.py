import random
import time

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


class RandomAI(ArtificialIntelligence):

    def create_next_action(self, game: Game) -> Action:
        return random.choice(list(Action))


class RandomWaitingAI(RandomAI):

    def create_next_action(self, game: Game) -> Action:
        time.sleep(10)
        return super().create_next_action(game)
