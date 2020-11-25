from multiprocessing import Value
from random import choice

from chillow.service.ai.pathfinding_ai import PathfindingAI
from chillow.service.ai.search_tree_ai import SearchTreeAI
from chillow.model.action import Action
from chillow.model.game import Game
from chillow.model.player import Player


class SearchTreePathfindingAI(PathfindingAI, SearchTreeAI):
    """ combination of the SearchTreeAI and the PathfindingAI, whereby the SearchTreeAI is prioritized. """

    def __init__(self, player: Player, max_speed: int, count_paths_to_check: int, depth: int,
                 distance_to_check: int = 0):
        """ Constructor that initializes the necessary attributes.

        Args:
            player: The player assigned to the AI.
            max_speed: The maximum speed the AI can reach.
            count_paths_to_check: The number of paths used to avoid dead ends.
            depth: Depth pre-calculating actions.
            distance_to_check: Distance an enemy player is allowed to be at maximum distance, so that he is taken into
                account in the calculations.
        """
        PathfindingAI.__init__(self, player, max_speed, count_paths_to_check)
        SearchTreeAI.__init__(self, player, depth, max_speed, distance_to_check=distance_to_check)

    def get_information(self) -> str:
        return "max_speed=" + str(self.max_speed) \
               + ", count_paths_to_check=" + str(self.count_paths_to_check) \
               + ", depth=" + str(self.get_depth()) \
               + ", distance_to_check=" + str(self.get_distance_to_check())

    def create_next_action(self, game: Game, return_value: Value):
        """ Creates the next action the AI will take. Saves the best result of the SearchTreeAI in the return_value
            already in between.

        Args:
            game: The game object in which the AI is located and contains the current status of the game.
            return_value: Object to save the result of the calculation.

        """
        self.turn_ctr += 1

        surviving_actions = super()._create_all_next_surviving_actions(game)
        if surviving_actions is not None and len(surviving_actions) > 0:
            return_value.value = choice(surviving_actions).get_index()

        action = self.find_actions_by_best_path_connection(surviving_actions, game)[0][0]\
            if len(surviving_actions) > 0 else Action.get_random_action()
        return_value.value = action.get_index()
