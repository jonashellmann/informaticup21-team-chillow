from abc import ABCMeta, abstractmethod

from chillow.model.game import Game
from chillow.model.player import Player
from chillow.model.action import ActionValue


class ArtificialIntelligence(metaclass=ABCMeta):

    def __init__(self, player: Player, max_speed: int = 10):
        self.player = player
        self.turn_ctr = 0
        self.max_speed = max_speed

    def get_information(self) -> str:
        return "max_speed=" + str(self.max_speed)

    @abstractmethod
    def create_next_action(self, game: Game, return_value: ActionValue):
        raise NotImplementedError
