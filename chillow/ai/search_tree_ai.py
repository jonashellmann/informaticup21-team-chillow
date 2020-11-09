from typing import List

from chillow.ai.search_tree_node import SearchTreeRoot
from chillow.ai.artificial_intelligence import ArtificialIntelligence
from chillow.model.action import Action
from chillow.model.game import Game
from chillow.model.player import Player


class SearchTreeAI(ArtificialIntelligence):

    def __init__(self, player: Player, depth: int, max_speed: int = 10, randomize: bool = False,
                 distance_to_check: int = 0):
        super().__init__(player, max_speed)
        self.__depth = depth
        self.__randomize = randomize
        self.__distance_to_check = distance_to_check

    def create_next_action(self, game: Game) -> Action:
        self.turn_ctr += 1
        root = SearchTreeRoot(game.copy())
        player_ids_to_watch = game.get_other_player_ids(self.player, self.__distance_to_check, True)
        combinations = Action.get_combinations(len(player_ids_to_watch))

        action = root.calculate_action(self.player, player_ids_to_watch, combinations, self.__depth, self.turn_ctr,
                                       True, [], self.max_speed, self.__randomize)
        return action if action is not None else Action.get_random_action()

    def _create_all_next_surviving_actions(self, game: Game) -> List[Action]:
        root = SearchTreeRoot(game.copy())
        player_ids_to_watch = game.get_other_player_ids(self.player, self.__distance_to_check, True)
        combinations = Action.get_combinations(len(player_ids_to_watch))

        search_tree_actions = []

        for action in Action.get_actions():
            if root.calculate_action(self.player, player_ids_to_watch, combinations, self.__depth, self.turn_ctr, True,
                                     [action], self.max_speed, True) is not None:
                search_tree_actions.append(action)

        return search_tree_actions
