from enum import Enum
import random


class Direction(Enum):
    left, right, up, down = range(4)

    @staticmethod
    def get_random_direction():
        return random.choice(list(Direction))
