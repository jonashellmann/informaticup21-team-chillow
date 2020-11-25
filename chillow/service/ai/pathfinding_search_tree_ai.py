from typing import List, Tuple, Optional
from multiprocessing import Value

from chillow.service.ai.pathfinding_ai import PathfindingAI
from chillow.service.ai.search_tree_ai import SearchTreeAI
from chillow.model.action import Action
from chillow.model.game import Game
from chillow.model.player import Player


class PathfindingSearchTreeAI(PathfindingAI, SearchTreeAI):
    """TODO

    Attributes:
        player: The player associated with this AI.
    """

    def __init__(self, player: Player, max_speed: int, count_paths_to_check: int, depth: int,
                 paths_tolerance: float = 0.75, distance_to_check: int = 0):
        PathfindingAI.__init__(self, player, max_speed, count_paths_to_check)
        SearchTreeAI.__init__(self, player, depth, max_speed, distance_to_check=distance_to_check)
        self.__paths_tolerance = paths_tolerance

    def get_information(self) -> str:
        return "max_speed=" + str(self._max_speed) \
               + ", paths_tolerance=" + str(self.__paths_tolerance) \
               + ", count_paths_to_check=" + str(self._get_count_paths_to_check()) \
               + ", depth=" + str(self._get_depth()) \
               + ", distance_to_check=" + str(self._get_distance_to_check())

    def create_next_action(self, game: Game, return_value: Value):
        self._turn_ctr += 1

        pathfinding_actions = self.create_next_actions_ranked(game)
        self.set_best_action(pathfinding_actions, [], return_value)
        search_tree_actions = super()._create_all_next_surviving_actions(game)
        self.set_best_action(pathfinding_actions, search_tree_actions, return_value)

    def set_best_action(self, pathfinding_actions: List[Tuple[Action, int]], search_tree_actions: List[Action],
                        return_value: Value):
        """TODO

        Args:
            pathfinding_actions:
            search_tree_actions:
            return_value:

        Returns:

        """
        best_action = self.get_best_action(pathfinding_actions, search_tree_actions)

        return_value.value = best_action.get_index() if best_action is not None else return_value.value

    def get_best_action(self, pathfinding_actions: List[Tuple[Action, int]],
                        search_tree_actions: List[Action]) -> Optional[Action]:
        """TODO

        Args:
            pathfinding_actions:
            search_tree_actions:

        Returns:

        """

        if search_tree_actions is None or len(search_tree_actions) == 0:
            if pathfinding_actions is not None and len(pathfinding_actions) > 0:
                return pathfinding_actions[0][0]
            return None
        elif pathfinding_actions is None or len(pathfinding_actions) == 0:
            return search_tree_actions[0]

        for (action, possible_paths) in pathfinding_actions:
            if action in search_tree_actions:
                if possible_paths == pathfinding_actions[0][1]:
                    return action  # best path and surviving guaranteed
                elif possible_paths >= pathfinding_actions[0][1] * self.__paths_tolerance:
                    return action  # good path and surviving guaranteed
                else:
                    break

        return pathfinding_actions[0][0]
