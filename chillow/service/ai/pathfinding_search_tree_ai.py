from typing import List, Tuple, Optional
from multiprocessing import Value

from chillow.service.ai.pathfinding_ai import PathfindingAI
from chillow.service.ai.search_tree_ai import SearchTreeAI
from chillow.model.action import Action
from chillow.model.game import Game
from chillow.model.player import Player


class PathfindingSearchTreeAI(PathfindingAI, SearchTreeAI):
    """ Combination of the PathfindingAI and the SearchTreeAI, whereby the PathfindingAi is prioritized.

    Attributes:
        player: The player associated with this AI.
    """

    def __init__(self, player: Player, max_speed: int, count_paths_to_check: int, depth: int,
                 paths_tolerance: float = 0.75, distance_to_check: int = 0):
        """ Creates a new object of the PathfindingSearchTreeAI.

        Args:
            player: The player assigned to the AI.
            max_speed: The maximum speed the AI can reach.
            count_paths_to_check: The number of paths used to avoid dead ends.
            depth: Depth pre-calculating actions.
            paths_tolerance: A tolerance, whereby more than just the best action is calculated. Actions which are
                worse, but within this tolerance, are also considered.
                depth: Number of player actions that are looked into the future.
            distance_to_check: Distance an enemy player is allowed to be at maximum distance, so that he is taken into
                account in the calculations.
        """
        PathfindingAI.__init__(self, player, max_speed, count_paths_to_check)
        SearchTreeAI.__init__(self, player, depth, max_speed, distance_to_check=distance_to_check)
        self.__paths_tolerance = paths_tolerance

    def get_information(self) -> str:
        """See base class."""
        return "max_speed=" + str(self._max_speed) \
               + ", paths_tolerance=" + str(self.__paths_tolerance) \
               + ", count_paths_to_check=" + str(self._get_count_paths_to_check()) \
               + ", depth=" + str(self._get_depth()) \
               + ", distance_to_check=" + str(self._get_distance_to_check())

    def create_next_action(self, game: Game, return_value: Value):
        """See base class."""
        self._turn_ctr += 1

        pathfinding_actions = self.create_next_actions_ranked(game)
        self.set_best_action(pathfinding_actions, [], return_value)
        search_tree_actions = super()._create_all_next_surviving_actions(game)
        self.set_best_action(pathfinding_actions, search_tree_actions, return_value)

    def set_best_action(self, pathfinding_actions: List[Tuple[Action, int]], search_tree_actions: List[Action],
                        return_value: Value):
        """ Saves the best action from the list of actions from PathfindingAI and SearchTreeAI.

        Args:
            pathfinding_actions: List of actions calculated by PathfindingAI.
            search_tree_actions: List of actions calculated by SearchTreeAI
            return_value: Object to save the result of the calculation.
        """
        best_action = self.get_best_action(pathfinding_actions, search_tree_actions)

        return_value.value = best_action.get_index() if best_action is not None else return_value.value

    def get_best_action(self, pathfinding_actions: List[Tuple[Action, int]],
                        search_tree_actions: List[Action]) -> Optional[Action]:
        """ Calculates the best action from the list of actions from PathfindingAI and SearchTreeAI.

        Args:
            pathfinding_actions: List of actions calculated by PathfindingAI.
            search_tree_actions: List of actions calculated by SearchTreeAI

        Returns:
            Best action if there is any.
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
