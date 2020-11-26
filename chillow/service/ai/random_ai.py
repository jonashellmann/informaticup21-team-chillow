import time
from multiprocessing import Value

from chillow.service.ai.artificial_intelligence import ArtificialIntelligence
from chillow.model.action import Action
from chillow.model.game import Game


class RandomAI(ArtificialIntelligence):
    """AI that randomly chooses an action ignoring the state of the game.

    Attributes:
        player: The player associated with this AI.
    """

    def create_next_action(self, game: Game, return_value: Value):
        """See base class."""
        self._turn_ctr += 1
        action = Action.get_random_action()
        return_value.value = action.get_index()

    def get_information(self) -> str:
        """See base class."""
        return ""


class RandomWaitingAI(RandomAI):
    """AI that randomly chooses an action ignoring the state of the game and waits five seconds.

    Attributes:
        player: The player associated with this AI.
    """

    def create_next_action(self, game: Game, return_value: Value):
        time.sleep(5)
        super().create_next_action(game, return_value)
