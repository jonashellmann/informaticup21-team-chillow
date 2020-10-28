import random
import os
import time
if not os.getenv("DEACTIVATE_PYGAME", False):
    import pygame

from chillow.ai.artificial_intelligence import ArtificialIntelligence
from chillow.model.action import Action
from chillow.model.game import Game


class RandomAI(ArtificialIntelligence):

    def create_next_action(self, game: Game) -> Action:
        return random.choice(list(Action))


class RandomWaitingAI(RandomAI):

    def create_next_action(self, game: Game) -> Action:
        if not os.getenv("DEACTIVATE_PYGAME", False):
            pygame.event.pump()
        time.sleep(5)
        return super().create_next_action(game)
