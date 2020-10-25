import chillow.game_services.exceptions as ex
from datetime import datetime


class Turn:

    def __init__(self, players, deadline):
        self.players = players
        self.playersWithAction = []
        self.deadline = deadline

    def action(self, player):
        d = datetime.now()
        if player in self.playersWithAction:
            raise ex.MultipleActionByPlayerError
        elif self.deadline < d:
            raise ex.DeadLineExceededException
        else:
            self.playersWithAction.append(player)
            if len(self.players) == len(self.playersWithAction):
                return True  # Turn ended
            return False  # Turn not ended
