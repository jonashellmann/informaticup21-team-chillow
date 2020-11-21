from abc import ABCMeta, abstractmethod
from multiprocessing import Value

from chillow.model.game import Game
from chillow.model.player import Player


class ArtificialIntelligence(metaclass=ABCMeta):

    def __init__(self, player: Player, max_speed: int = 10):
        self.player = player
        self.turn_ctr = 0
        self.max_speed = max_speed

    def get_information(self) -> str:
        return "max_speed=" + str(self.max_speed)

    # Important: To be able to share the result of this calculation across multiple processes, it is necessary
    # that the result is stored as in integer in the "value"-variable of the "return_value"-Parameter.
    # This means that no "return" statement is used.
    # The integer value represents the index of the calculated action in the Action enumeration.
    # For this transformation there are two methods:
    # Action -> int: action.get_index()
    # int -> Action: Action.get_by_index(index)
    @abstractmethod
    def create_next_action(self, game: Game, return_value: Value):
        raise NotImplementedError
