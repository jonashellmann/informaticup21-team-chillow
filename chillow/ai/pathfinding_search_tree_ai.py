from typing import List, Tuple

from chillow.ai.pathfinding_ai import PathfindingAI
from chillow.ai.search_tree_node import SearchTreeRoot
from chillow.model.action import Action
from chillow.model.game import Game
from chillow.model.player import Player


class PathfindingSearchTreeAI(PathfindingAI):

    def __init__(self, player: Player, max_speed: int, count_paths_to_check: int, depth: int,
                 paths_tolerance: float = 0.75):
        super().__init__(player, max_speed, count_paths_to_check)
        self.__depth = depth
        self.paths_tolerance = paths_tolerance

    def create_next_action(self, game: Game) -> Action:
        self.turn_ctr += 1

        pathfinding_actions: List[Tuple[Action, int]] = self.create_next_actions_ranked(game)

        root = SearchTreeRoot(game.copy())
        combinations = Action.get_combinations(len(game.get_other_players(self.player)))

        search_tree_actions = []

        for action in Action.get_actions():
            if root.calculate_action(self.player, combinations, self.__depth, self.turn_ctr, True, [action],
                                     self.max_speed, True) is not None:
                search_tree_actions.append(action)

        return self.get_best_action(pathfinding_actions, search_tree_actions)

    def get_best_action(self, pathfinding_actions: List[Tuple[Action, int]],
                        search_tree_actions: List[Action]) -> Action:
        for (action, possible_paths) in pathfinding_actions:
            if action in search_tree_actions:
                if possible_paths == pathfinding_actions[0][1]:
                    return action  # best path and surviving guaranteed
                elif possible_paths >= pathfinding_actions[0][1] * self.paths_tolerance:
                    return action  # good path and surviving guaranteed
                else:
                    break

        return pathfinding_actions[0][0]
