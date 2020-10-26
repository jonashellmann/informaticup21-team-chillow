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
