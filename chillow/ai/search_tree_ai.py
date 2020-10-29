from itertools import product
from copy import deepcopy
from typing import Any

from chillow.ai.search_tree_node import SearchTreeRoot
from chillow.ai.artificial_intelligence import ArtificialIntelligence
from chillow.model.action import Action
from chillow.model.game import Game
from chillow.model.player import Player


class SearchTreeAI(ArtificialIntelligence):

    def __init__(self, player: Player, depth: int):
        super().__init__(player)
        self.__player = player
        self.__depth = depth
        self.__turn_counter = 0

    def create_next_action(self, game: Game) -> Action:
        self.__turn_counter += 1
        root = SearchTreeRoot(deepcopy(game))
        combinations = SearchTreeAI.__get_combinations(len(game.get_other_players()))

        return root.calculate_action(self.__player, combinations, self.__depth, self.__turn_counter)

    @staticmethod
    def __get_combinations(player_count: int) -> list[tuple[Any]]:
        return list(product(list(Action), repeat=player_count))
