from dataclasses import dataclass

from .direction import Direction


@dataclass
class Player:

    id: str
    x: int
    y: int
    direction: Direction
    speed: int
    active: bool
    name: str
