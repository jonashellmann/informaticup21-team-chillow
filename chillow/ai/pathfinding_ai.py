from typing import List, Tuple
from random import shuffle
from numpy import arange

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

    def __init__(self, player: Player, game: Game, max_speed, count_paths_to_check):
        super().__init__(player, max_speed)
        self.__game = game
        self.count_paths_to_check = count_paths_to_check

    def create_next_action(self, game: Game) -> Action:
        super().create_next_action(game)

        self.__game = game
        game_service = GameService(game)
        game_service.turn.turn_ctr = self.turn_ctr

        surviving_actions = self.find_surviving_actions(game_service)

        if len(surviving_actions) == 1:
            return surviving_actions[0]
        else:
            return self.find_action_by_best_path_connection(surviving_actions) if len(
                surviving_actions) > 0 else Action.get_random_action()

    def find_action_by_best_path_connection(self, actions: List[Action]) -> Action:
        shuffle(actions)
        best_action: Tuple[Action, int] = (actions[0], 0)
        free_cells_for_pathfinding = self.get_random_free_cells_from_playground()

        path_finder = BestFirst(diagonal_movement=DiagonalMovement.never)

        for action in actions:
            game_copy = self.__game.copy()
            game_service = GameService(game_copy)
            try:
                player = game_service.game.get_player_by_id(self.player.id)
                game_service.visited_cells_by_player[player.id] = game_service.get_and_visit_cells(player, action)
            except InvalidPlayerMoveException:
                continue

            matrix = self.translate_cell_matrix_to_pathfinding_matrix(game_copy)
            current_possible_paths = 0
            for i in range(len(free_cells_for_pathfinding)):
                grid = Grid(matrix=matrix)
                start = grid.node(player.x, player.y)
                end = grid.node(free_cells_for_pathfinding[i][0], free_cells_for_pathfinding[i][1])
                path, runs = path_finder.find_path(start, end, grid)
                if len(path) > 0:
                    current_possible_paths += 1
                if current_possible_paths + len(free_cells_for_pathfinding) - i <= best_action[1]:  # can't be better
                    break
            if len(best_action) == 0 or best_action[1] < current_possible_paths:
                best_action = (action, current_possible_paths)
            if best_action[1] == len(free_cells_for_pathfinding):  # best possible action already found
                return best_action[0]

        return best_action[0]

    def get_random_free_cells_from_playground(self) -> List[Tuple[int, int]]:
        free_cells: List[(int, int)] = []
        for x in range(self.__game.height):
            for y in range(self.__game.width):
                if self.__game.cells[y][x].players is None or len(self.__game.cells[y][x].players) == 0:
                    free_cells.append((x, y))
        shuffle(free_cells)
        return free_cells[:min(self.count_paths_to_check, len(free_cells))]

    def get_evenly_distributed_free_cells_from_playground(self) -> List[Tuple[int, int]]:
        free_cells: List[(int, int)] = []
        count_cells = self.__game.width * self.__game.height
        evenly_distributed_points = arange(0, count_cells, int(count_cells / self.count_paths_to_check))
        for point in evenly_distributed_points:
            x = point % self.__game.width + 5
            y = int(point / self.__game.width)
            if self.__game.cells[y][x].players is None or len(self.__game.cells[y][x].players) == 0:
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
