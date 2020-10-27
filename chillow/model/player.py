from dataclasses import dataclass

from chillow.model.direction import Direction


@dataclass
class Player:

    id: int
    x: int  # The column in which the player is right now. The leftmost column has index 0.
    y: int  # The row in which the player is right now. The column at the top has index 0.
    direction: Direction
    speed: int
    active: bool
    name: str
