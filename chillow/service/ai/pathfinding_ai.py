import operator
from multiprocessing import Value
from typing import List, Tuple, Optional
from random import shuffle

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.best_first import BestFirst

from chillow.service.ai import NotKillingItselfAI
from chillow.exceptions import InvalidPlayerMoveException
from chillow.model.action import Action
from chillow.model.game import Game
from chillow.model.player import Player
from chillow.service.game_service import GameService


class PathfindingAI(NotKillingItselfAI):

    def __init__(self, player: Player, max_speed: int, count_paths_to_check: int):
        super().__init__(player, [], max_speed, 0)
        self.count_paths_to_check = count_paths_to_check

    def get_information(self) -> str:
        return "max_speed=" + str(self.max_speed) \
               + ", count_paths_to_check=" + str(self.count_paths_to_check)

    def create_next_action(self, game: Game, return_value: Value):
        self.turn_ctr += 1
        actions = self.create_next_actions_ranked(game)
        action = actions[0][0] if actions is not None and len(actions) > 0 else Action.get_random_action()
        return_value.value = list(Action).index(action)

    def create_next_actions_ranked(self, game: Game) -> Optional[List[Tuple[Action, int]]]:
        game_service = GameService(game)
        game_service.turn.turn_ctr = self.turn_ctr

        surviving_actions = self.find_surviving_actions(game_service)

        return self.find_actions_by_best_path_connection(surviving_actions, game)

    def find_actions_by_best_path_connection(self, actions: List[Action], game: Game) -> Optional[
            List[Tuple[Action, int]]]:
        if actions is None or len(actions) == 0:
            return None

        shuffle(actions)
        actions_with_possible_paths: List[Tuple[Action, int]] = []
        free_cells_for_pathfinding = self.get_random_free_cells_from_playground(game)

        path_finder = BestFirst(diagonal_movement=DiagonalMovement.never)

        for action in actions:
            game_copy = game.copy()
            game_service = GameService(game_copy)
            try:
                player = game_service.game.get_player_by_id(self.player.id)
                game_service.visited_cells_by_player[player.id] = game_service.get_and_visit_cells(player, action)
            except InvalidPlayerMoveException:
                continue

            matrix = game_copy.translate_cell_matrix_to_pathfinding_matrix()
            current_possible_paths = 0
            length_free_cells = len(free_cells_for_pathfinding)
            for i in range(length_free_cells):
                grid = Grid(matrix=matrix)
                start = grid.node(player.x, player.y)
                end = grid.node(free_cells_for_pathfinding[i][0], free_cells_for_pathfinding[i][1])
                path, runs = path_finder.find_path(start, end, grid)
                if len(path) > 0:
                    current_possible_paths += 1

            actions_with_possible_paths.append((action, current_possible_paths))

        actions_with_possible_paths.sort(key=operator.itemgetter(1), reverse=True)
        return actions_with_possible_paths

    def get_random_free_cells_from_playground(self, game: Game) -> List[Tuple[int, int]]:
        free_cells: List[(int, int)] = []
        for x in range(game.width):
            for y in range(game.height):
                if game.cells[y][x].players is None or len(game.cells[y][x].players) == 0:
                    free_cells.append((x, y))
        shuffle(free_cells)
        return free_cells[:min(self.count_paths_to_check, len(free_cells))]
