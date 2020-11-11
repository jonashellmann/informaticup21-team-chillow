from chillow.service.ai.pathfinding_ai import PathfindingAI
from chillow.service.ai.search_tree_ai import SearchTreeAI
from chillow.model.action import Action
from chillow.model.game import Game
from chillow.model.player import Player


class SearchTreePathfindingAI(PathfindingAI, SearchTreeAI):

    def __init__(self, player: Player, max_speed: int, count_paths_to_check: int, depth: int,
                 distance_to_check: int = 0):
        PathfindingAI.__init__(self, player, max_speed, count_paths_to_check)
        SearchTreeAI.__init__(self, player, depth, max_speed, distance_to_check=distance_to_check)

    def create_next_action(self, game: Game) -> Action:
        self.turn_ctr += 1

        surviving_actions = super()._create_all_next_surviving_actions(game)

        return self.find_actions_by_best_path_connection(surviving_actions, game)[0][0] if len(
                surviving_actions) > 0 else Action.get_random_action()
