from itertools import product
from copy import deepcopy
from typing import Any, List, Tuple

from chillow.ai.search_tree_node import SearchTreeRoot
from chillow.ai.artificial_intelligence import ArtificialIntelligence
from chillow.model.action import Action
from chillow.model.game import Game
from chillow.model.player import Player


class SearchTreeAI(ArtificialIntelligence):

    def __init__(self, player: Player, depth: int, max_speed: int = 10, randomize: bool = False):
        super().__init__(player, max_speed)
        self.__depth = depth
        self.__randomize = randomize

    def create_next_action(self, game: Game) -> Action:
        super().create_next_action(game)
        root = SearchTreeRoot(deepcopy(game))
        combinations = SearchTreeAI.__get_combinations(len(game.get_other_players(self.player)))

        action = root.calculate_action(self.player, combinations, self.__depth, self.turn_ctr, self.max_speed,
                                       self.__randomize)
        return action if action is not None else Action.get_random_action()

    @staticmethod
    def __get_combinations(player_count: int) -> List[Tuple[Any]]:
        return list(product(Action.get_actions(), repeat=player_count))
