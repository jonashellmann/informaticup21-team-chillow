import pickle
from abc import ABCMeta, abstractmethod
from typing import List

from chillow.exceptions import InvalidPlayerMoveException
from chillow.model.action import Action
from chillow.model.game import Game
from chillow.model.player import Player
from chillow.service.game_service import GameService


class ArtificialIntelligence(metaclass=ABCMeta):

    def __init__(self, player: Player, max_speed: int = 10):
        self.player = player
        self.turn_ctr = 0
        self.max_speed = max_speed

    @abstractmethod
    def create_next_action(self, game: Game) -> Action:
        self.turn_ctr += 1

    def find_surviving_actions(self, game_service: GameService) -> List[Action]:
        result: List[Action] = []
        for action in Action:  # select a surviving action
            gs_copy = pickle.loads(pickle.dumps(game_service))
            try:
                player = gs_copy.game.get_player_by_id(self.player.id)
                if player.speed == self.max_speed and action == Action.speed_up:
                    continue
                gs_copy.visited_cells_by_player[player.id] = gs_copy.get_and_visit_cells(player, action)
            except InvalidPlayerMoveException:
                continue
            gs_copy.check_and_set_died_players()
            if player.active:
                result += [action]

        return result
