import random
from dataclasses import dataclass
from enum import Enum
from itertools import product
from typing import Any, List, Tuple


class Action(Enum):
    turn_left, turn_right, speed_up, slow_down, change_nothing = range(5)

    @staticmethod
    def get_actions(randomize: bool = False):
        if randomize:
            return Action.__get_random_actions()
        return list(Action)

    @staticmethod
    def get_random_action():
        return random.choice(Action.get_actions())

    @staticmethod
    def __get_random_actions():
        actions = Action.get_actions()
        random.shuffle(actions)
        return actions

    @staticmethod
    def get_combinations(player_count: int) -> List[Tuple[Any]]:
        return list(product(Action.get_actions(), repeat=player_count))


@dataclass
class ActionValue:
    action: Action = None

