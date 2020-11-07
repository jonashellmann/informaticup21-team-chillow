from chillow.ai.pathfinding_ai import PathfindingAI
from chillow.ai.search_tree_node import SearchTreeRoot
from chillow.model.action import Action
from chillow.model.game import Game
from chillow.model.player import Player


class PathfindingSearchTreeAI(PathfindingAI):

    def __init__(self, player: Player, max_speed: int, count_paths_to_check: int, depth: int):
        super().__init__(player, max_speed, count_paths_to_check)
        self.__depth = depth

    def create_next_action(self, game: Game) -> Action:
        self.turn_ctr += 1
        root = SearchTreeRoot(game.copy())
        combinations = Action.get_combinations(len(game.get_other_players(self.player)))

        surviving_actions = []

        for action in Action.get_actions():
            if root.calculate_action(self.player, combinations, self.__depth, self.turn_ctr, True, [action],
                                     self.max_speed, True) is not None:
                surviving_actions.append(action)

        return self.find_action_by_best_path_connection(surviving_actions, game)[0][0] if len(
                surviving_actions) > 0 else Action.get_random_action()
