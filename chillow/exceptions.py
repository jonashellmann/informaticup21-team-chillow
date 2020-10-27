from chillow.model.player import Player


class MultipleActionByPlayerError(Exception):

    def __init__(self, player: Player):
        print("Player " + str(player.name) + ", id " + str(
            player.id) + " did more than one action this turn and is inactive now")


class DeadLineExceededException(Exception):

    def __init__(self, player: Player):
        print(
            "Player " + str(player.name) + ", id " + str(player.id) + " exceeded the Deadline and is inactive now")


class PlayerSpeedNotInRangeException(Exception):

    def __init__(self, player: Player):
        print(
            "Player " + str(player.name) + ", id " + str(player.id) + " reached invalid speed and is inactive now")


class PlayerOutsidePlaygroundException(Exception):

    def __init__(self, player: Player):
        print(
            "Player " + str(player.name) + ", id " + str(player.id) + " outside Playground and is inactive now")


class WrongGameWidthException(Exception):

    def __init__(self, width: int, actual_width: int):
        print("Width of game should be " + str(width) + ", but is " + str(actual_width))


class WrongGameHeightException(Exception):

    def __init__(self, height: int, actual_height: int):
        print("Height of game should be " + str(height) + ", but is " + str(actual_height))


class OwnPlayerMissingException(Exception):

    def __init__(self):
        print("The player defined as your player is not present in game")
