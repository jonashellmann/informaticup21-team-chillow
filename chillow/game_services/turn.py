from typing import List

import chillow.game_services.exceptions as ex
from chillow.model.player import Player
from datetime import datetime, timedelta


class Turn:

    def __init__(self, players: List[Player], deadline):
        self.players = players.copy()
        self.playersWithPendingAction = players.copy()
        self.deadline = deadline
        self.turn_ctr = 1

    def action(self, player):
        if player not in self.playersWithPendingAction:
            raise ex.MultipleActionByPlayerError(player)
        # elif self.deadline < datetime.now():
        #    raise ex.DeadLineExceededException(player)
        else:
            self.playersWithPendingAction.remove(player)
            if len(self.playersWithPendingAction) == 0:
                self.turn_ctr += 1
                self.deadline = datetime.now() + timedelta(0, 180)
                for player in self.players:
                    if player.active:
                        self.playersWithPendingAction.append(player)
                return True  # Turn ended
            return False  # Turn not ended
