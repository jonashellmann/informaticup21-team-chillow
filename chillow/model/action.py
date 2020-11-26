import random
from enum import Enum
from itertools import product
from typing import Any, List, Tuple


class Action(Enum):
    """Enum to represent all possible actions which a player can perform to in a game."""

    turn_left, turn_right, speed_up, slow_down, change_nothing = range(5)

    @staticmethod
    def get_actions(randomize: bool = False):
        """Returns all actions defined in this enum.

        Args:
            randomize: If this flag is true, the returned list is not in order but shuffled randomly.

        Returns:
            Returns all actions defined in this enum.
        """

        if randomize:
            return Action.__get_random_actions()
        return list(Action)

    @staticmethod
    def get_random_action():
        """Randomly chooses one of the defined actions in this enum.

        Returns:
            A random action.
        """

        return random.choice(Action.get_actions())

    @staticmethod
    def __get_random_actions():
        actions = Action.get_actions()
        random.shuffle(actions)
        return actions

    @staticmethod
    def get_combinations(player_count: int) -> List[Tuple[Any]]:
        """Creates all combinations of actions.

        E.g. if the parameter is 3, the returned list looks like following and contains 5^3 tuples.
        [(left, left, left), (left, left, right), ..., (change_nothing, change_nothing, change_nothing)]

        Args:
            player_count: Defines how many actions should be in one tuple.

        Returns:
            A list of tuples with all possible combinations of actions.
        """

        return list(product(Action.get_actions(), repeat=player_count))

    @staticmethod
    def get_by_index(index: int):
        """Finds an action by its position in the enum.

        Args:
            index: The index of the enum element.

        Returns:
            The enum element at the index.
        """

        return Action.get_actions()[index]

    def get_index(self):
        """Gets the index of an element in the enum.

        Returns:
            The index of an element in the enum
        """

        return Action.get_actions().index(self)

    @staticmethod
    def get_default():
        """Defines the default action.

        Returns:
            The defined default action.
        """

        return Action.change_nothing
