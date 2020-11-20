import time
from multiprocessing import Value

from chillow.service.ai.artificial_intelligence import ArtificialIntelligence
from chillow.model.action import Action
from chillow.model.game import Game


class RandomAI(ArtificialIntelligence):

    def create_next_action(self, game: Game, return_value: Value):
        self.turn_ctr += 1
        action = Action.get_random_action()
        return_value.value = list(Action).index(action)

    def get_information(self) -> str:
        return ""


class RandomWaitingAI(RandomAI):

    def create_next_action(self, game: Game, return_value: Value):
        time.sleep(5)
        super().create_next_action(game, return_value)
