from abc import ABCMeta, abstractmethod
from multiprocessing import Value

from chillow.model.game import Game
from chillow.model.player import Player


class ArtificialIntelligence(metaclass=ABCMeta):
    """Abstract base-class for AI implementations.

    Attributes:
        player: The player associated with this AI.
    """

    def __init__(self, player: Player, max_speed: int = 10):
        self.player = player
        self._turn_ctr = 0
        self._max_speed = max_speed

    def get_information(self) -> str:
        """Creates a string containing information about the attributes of the AI.

        Returns:
            A string containing information about the attributes of the AI.
        """

        return "max_speed=" + str(self._max_speed)

    @abstractmethod
    def create_next_action(self, game: Game, return_value: Value):
        """This method is used to calculate the next action for the player in a given game.

        To be able to share the result of this calculation across multiple processes, it is necessary
        that the result is stored as in integer in the "value"-variable of the "return_value"-Parameter.
        This means that no "return" statement is used.
        The integer value represents the index of the calculated action in the Action enumeration.
        For this transformation there are two methods:
        Action -> int: action.get_index()
        int -> Action: Action.get_by_index(index)

        Args:
            game: The game state for which the next action of the AI player should be calculated for.
            return_value: The value in which the return value should be stored.
        """
        pass
