from enum import Enum
import random


class Direction(Enum):
    """Enum to represent all possible directions in which a player can be directed to in a game."""
    left, right, up, down = range(4)

    @staticmethod
    def get_random_direction():
        """Randomly chooses one of the defined directions in this enum.

        Returns:
            A random direction.
        """
        return random.choice(list(Direction))
