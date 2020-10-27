import random
import time
import os
if not os.getenv("DEACTIVATE_PYGAME", False):
    import pygame

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
        if not os.getenv("DEACTIVATE_PYGAME", False):
            pygame.event.pump()
        time.sleep(5)
        return super().create_next_action(game)
