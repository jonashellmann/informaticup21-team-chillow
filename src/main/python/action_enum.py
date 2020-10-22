from enum import Enum


class ActionEnum(Enum):
    turn_left, turn_right, speed_up, slow_down, change_nothing = range(5)
