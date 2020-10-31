from typing import List, Tuple
from random import randint, shuffle
from numpy import arange

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from chillow.ai.artificial_intelligence import ArtificialIntelligence
from chillow.model.action import Action
from chillow.model.game import Game
from chillow.model.player import Player
from chillow.service.game_service import GameService


class PathfindingAI(ArtificialIntelligence):

    def __init__(self, player: Player, game: Game, max_speed, count_paths_to_check):
        super().__init__(player)
        self.__game = game
        self.turn_ctr = 0
        self.max_speed = max_speed
        self.count_paths_to_check = count_paths_to_check

    def create_next_action(self, game: Game) -> Action:
        self.turn_ctr += 1
        self.__game = game
        game_service = GameService(game)
        game_service.turn.turn_ctr = self.turn_ctr

        surviving_actions = self.find_surviving_actions(game_service)

        return self.find_action_by_best_path_connection(surviving_actions) if len(
            surviving_actions) > 0 else Action.get_random_action()

    def find_action_by_best_path_connection(self, actions: List[Action]) -> Action:
        shuffle(actions)
        best_action: Tuple[Action, int] = (actions[0], 0)
        free_cells_for_pathfinding = self.get_random_free_cells_from_playground()

        path_finder = AStarFinder(diagonal_movement=DiagonalMovement.never)

        for action in actions:
            game_copy = self.__game.copy()
            game_service = GameService(game_copy)
            try:
                player = game_service.game.get_player_by_id(self.player.id)
                game_service.visited_cells_by_player[player.id] = game_service.get_and_visit_cells(player, action)
            except Exception:
                continue

            matrix = self.translate_cell_matrix_to_pathfinding_matrix(game_copy)
            current_possible_paths = 0
            for free_cell in free_cells_for_pathfinding:
                grid = Grid(matrix=matrix)
                start = grid.node(player.x, player.y)
                end = grid.node(free_cell[0], free_cell[1])
                path, runs = path_finder.find_path(start, end, grid)
                if len(path) > 0:
                    current_possible_paths += 1
            if len(best_action) == 0 or best_action[1] < current_possible_paths:
                best_action = (action, current_possible_paths)

        return best_action[0]

    def get_random_free_cells_from_playground(self) -> List[Tuple[int, int]]:
        # Todo: Find minimum Number of free Cells
        free_cells: List[(int, int)] = []
        for x in range(self.__game.height):
            for y in range(self.__game.width):
                if self.__game.cells[y][x].players is None or len(self.__game.cells[y][x].players) == 0:
                    free_cells.append((x, y))
        shuffle(free_cells)
        return free_cells[:min(self.count_paths_to_check, len(free_cells))]

    def get_aranged_free_cells_from_playground(self) -> List[Tuple[int, int]]:
        free_cells: List[(int, int)] = []
        count_cells = self.__game.width * self.__game.height
        evenly_aranged_points = arange(0, count_cells, int(count_cells / self.count_paths_to_check))
        for point in evenly_aranged_points:
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
