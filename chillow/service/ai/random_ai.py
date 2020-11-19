import time
from typing import List

from chillow.service.ai.artificial_intelligence import ArtificialIntelligence
from chillow.model.action import Action
from chillow.model.game import Game
from chillow.service.ai.return_value import ReturnValue


class RandomAI(ArtificialIntelligence):

    def create_next_action(self, game: Game, return_value: ReturnValue):
        self.turn_ctr += 1
        return_value.action = Action.get_random_action()

    def get_information(self) -> str:
        return ""


class RandomWaitingAI(RandomAI):

    def create_next_action(self, game: Game, return_value: ReturnValue):
        time.sleep(5)
        super().create_next_action(game, return_value)
