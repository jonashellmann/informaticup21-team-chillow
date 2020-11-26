from dataclasses import dataclass

from chillow.model.direction import Direction


@dataclass
class Player:
    """Represents a player in a game.

    Attributes:
        id: The ID of the player in a game.
        x: The position on the x axis.
        y: The position on the y axis.
        direction: The direction to which the player is looking at.
        speed: The speed of the player.
        active: A flag indicating whether the player is still active.
        name:
            The name of the player.
            This value is empty as long as the player is active.
    """

    id: int
    x: int
    y: int
    direction: Direction
    speed: int
    active: bool
    name: str
