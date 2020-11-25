from multiprocessing import Value
from random import choice

from chillow.service.ai.pathfinding_ai import PathfindingAI
from chillow.service.ai.search_tree_ai import SearchTreeAI
from chillow.model.action import Action
from chillow.model.game import Game
from chillow.model.player import Player


class SearchTreePathfindingAI(PathfindingAI, SearchTreeAI):
    """This AI combines the SearchTreeAI and the PathfindingAI by favoring the former.

    Therefore it finds all actions that let the player survive the next rounds by using the SearchTreeAI and
    afterwards lets the PathfindingAI check which of these is the best action to perform.

    Attributes:
        player: The player associated with this AI.
    """

    def __init__(self, player: Player, max_speed: int, count_paths_to_check: int, depth: int,
                 distance_to_check: int = 0):
        PathfindingAI.__init__(self, player, max_speed, count_paths_to_check)
        SearchTreeAI.__init__(self, player, depth, max_speed, distance_to_check=distance_to_check)

    def get_information(self) -> str:
        return "max_speed=" + str(self._max_speed) \
               + ", count_paths_to_check=" + str(self._get_count_paths_to_check()) \
               + ", depth=" + str(self._get_depth()) \
               + ", distance_to_check=" + str(self._get_distance_to_check())

    def create_next_action(self, game: Game, return_value: Value):
        self._turn_ctr += 1

        surviving_actions = super()._create_all_next_surviving_actions(game)
        if surviving_actions is not None and len(surviving_actions) > 0:
            return_value.value = choice(surviving_actions).get_index()

        action = self.find_actions_by_best_path_connection(surviving_actions, game)[0][0]\
            if len(surviving_actions) > 0 else Action.get_random_action()
        return_value.value = action.get_index()
