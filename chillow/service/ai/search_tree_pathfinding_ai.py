from multiprocessing import Value
from random import choice

from chillow.service.ai.pathfinding_ai import PathfindingAI
from chillow.service.ai.search_tree_ai import SearchTreeAI
from chillow.model.action import Action
from chillow.model.game import Game
from chillow.model.player import Player
from chillow.service.game_service import GameService


class SearchTreePathfindingAI(PathfindingAI, SearchTreeAI):
    """This AI combines the SearchTreeAI and the PathfindingAI by favoring the former.

    Therefore it finds all actions that let the player survive the next rounds by using the SearchTreeAI and
    afterwards lets the PathfindingAI check which of these is the best action to perform.

    Attributes:
        player: The player associated with this AI.
    """

    def __init__(self, player: Player, max_speed: int, count_paths_to_check: int, depth: int,
                 distance_to_check: int = 0):
        """Creates a new object of the SearchTreePathfindingAI.

        Args:
            player: The player assigned to the AI.
            max_speed: The maximum speed the AI can reach.
            count_paths_to_check: The number of paths used to avoid dead ends.
            depth: Number of pre-calculating actions.
            distance_to_check:
                Distance an enemy player is allowed to be at maximum distance, so that he is taken into
                account in the calculations.
        """
        PathfindingAI.__init__(self, player, max_speed, count_paths_to_check)
        SearchTreeAI.__init__(self, player, depth, max_speed, distance_to_check=distance_to_check)

    def get_information(self) -> str:
        """See base class."""
        return "max_speed=" + str(self._max_speed) \
               + ", count_paths_to_check=" + str(self._get_count_paths_to_check()) \
               + ", depth=" + str(self._get_depth()) \
               + ", distance_to_check=" + str(self._get_distance_to_check())

    def create_next_action(self, game: Game, return_value: Value):
        """See base class."""
        self._turn_ctr += 1

        surviving_actions = self.create_all_next_surviving_actions(game)
        if surviving_actions is not None and len(surviving_actions) > 0:
            return_value.value = choice(surviving_actions).get_index()
            return_value.value = self.find_actions_by_best_path_connection(surviving_actions, game)[0][0].get_index()
        else:
            surviving_pathfinding_actions = self.find_actions_by_best_path_connection(
                self.find_surviving_actions(GameService(game), 1), game)
            return_value.value = surviving_pathfinding_actions[0][0].get_index() \
                if surviving_pathfinding_actions is not None and len(surviving_pathfinding_actions) > 0 \
                else Action.get_default().get_index()
