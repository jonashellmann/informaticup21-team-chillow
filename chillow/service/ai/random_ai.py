import time

from chillow.service.ai.artificial_intelligence import ArtificialIntelligence
from chillow.model.action import Action
from chillow.model.game import Game


class RandomAI(ArtificialIntelligence):

    def create_next_action(self, game: Game) -> Action:
        self.turn_ctr += 1
        return Action.get_random_action()

    def get_information(self) -> str:
        return ""


class RandomWaitingAI(RandomAI):

    def create_next_action(self, game: Game) -> Action:
        time.sleep(5)
        return super().create_next_action(game)
