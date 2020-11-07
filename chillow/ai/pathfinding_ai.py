from typing import List, Tuple, Optional
from random import shuffle
from numpy import arange, operator

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.best_first import BestFirst

from chillow.ai.artificial_intelligence import ArtificialIntelligence
from chillow.exceptions import InvalidPlayerMoveException
from chillow.model.action import Action
from chillow.model.game import Game
from chillow.model.player import Player
from chillow.service.game_service import GameService


class PathfindingAI(ArtificialIntelligence):

    def __init__(self, player: Player, max_speed: int, count_paths_to_check: int):
        super().__init__(player, max_speed)
        self.count_paths_to_check = count_paths_to_check

    def create_next_action(self, game: Game) -> Action:
        self.turn_ctr += 1

        game_service = GameService(game)
        game_service.turn.turn_ctr = self.turn_ctr

        surviving_actions = self.find_surviving_actions(game_service)

        if len(surviving_actions) == 1:
            return surviving_actions[0]
        else:
            return self.find_action_by_best_path_connection(surviving_actions, game) if len(
                surviving_actions) > 0 else Action.get_random_action()

    def find_action_by_best_path_connection(self, actions: List[Action], game: Game) -> Optional[
            List[Tuple[Action, int]]]:
        if actions is None or len(actions) == 0:
            return None

        shuffle(actions)
        best_actions: List[Tuple[Action, int]] = []
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

            matrix = self.translate_cell_matrix_to_pathfinding_matrix(game_copy)
            current_possible_paths = 0
            length_free_cells = len(free_cells_for_pathfinding)
            for i in range(length_free_cells):
                grid = Grid(matrix=matrix)
                start = grid.node(player.x, player.y)
                end = grid.node(free_cells_for_pathfinding[i][0], free_cells_for_pathfinding[i][1])
                path, runs = path_finder.find_path(start, end, grid)
                if len(path) > 0:
                    current_possible_paths += 1

            best_actions.append((action, current_possible_paths))

        return best_actions.sort(key=operator.itemgetter(1))

    def get_random_free_cells_from_playground(self, game: Game) -> List[Tuple[int, int]]:
        free_cells: List[(int, int)] = []
        for x in range(game.width):
            for y in range(game.height):
                if game.cells[y][x].players is None or len(game.cells[y][x].players) == 0:
                    free_cells.append((x, y))
        shuffle(free_cells)
        return free_cells[:min(self.count_paths_to_check, len(free_cells))]

    def get_evenly_distributed_free_cells_from_playground(self, game: Game) -> List[Tuple[int, int]]:
        free_cells: List[(int, int)] = []
        count_cells = game.width * game.height
        evenly_distributed_points = arange(0, count_cells, int(count_cells / self.count_paths_to_check))
        for point in evenly_distributed_points:
            x = point % game.width + 5
            y = int(point / game.width)
            if game.cells[y][x].players is None or len(game.cells[y][x].players) == 0:
                free_cells.append((x, y))
        return free_cells

    @staticmethod
    def translate_cell_matrix_to_pathfinding_matrix(game: Game) -> List[List[int]]:
        matrix = [[1 for _ in range(game.width)] for _ in range(game.height)]
        for i in range(len(game.cells)):
            for j in range(len(game.cells[i])):
                if game.cells[i][j].players is not None and len(game.cells[i][j].players) > 0:
                    matrix[i][j] = 0  # Collision cell
        return matrix
