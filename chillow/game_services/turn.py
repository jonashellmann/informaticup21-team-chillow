from typing import List

import chillow.game_services.exceptions as ex
from chillow.model.player import Player
from datetime import datetime


class Turn:

    def __init__(self, players: List[Player], deadline):
        self.players = players.copy()
        self.playersWithPendingAction = players.copy()
        self.deadline = deadline

    def action(self, player):
        d = datetime.now()
        if player not in self.playersWithPendingAction:
            raise ex.MultipleActionByPlayerError
        elif self.deadline < d:
            raise ex.DeadLineExceededException
        else:
            self.playersWithPendingAction.remove(player)
            if len(self.playersWithPendingAction) == 0:
                for player in self.players:
                    if player.active:
                        self.playersWithPendingAction.append(player)
                return True  # Turn ended
            return False  # Turn not ended
