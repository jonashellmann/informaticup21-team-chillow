import time
from multiprocessing import Value

from chillow.service.ai.artificial_intelligence import ArtificialIntelligence
from chillow.model.action import Action
from chillow.model.game import Game


class RandomAI(ArtificialIntelligence):
    """ AI making random decisions. """

    def create_next_action(self, game: Game, return_value: Value):
        """ Calculates a random action and returns it.

        Args:
            game: The game object in which the AI is located and contains the current status of the game.
            return_value: Object to save the result of the calculation.

        Returns:
            Returns an action.
        """
        self.turn_ctr += 1
        action = Action.get_random_action()
        return_value.value = action.get_index()

    def get_information(self) -> str:
        return ""


class RandomWaitingAI(RandomAI):
    """ Variant of RandomAI, but waiting a time after the action. """

    def create_next_action(self, game: Game, return_value: Value):
        time.sleep(5)
        super().create_next_action(game, return_value)
