from typing import List, Tuple
from random import randint

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from chillow.ai.artificial_intelligence import ArtificialIntelligence
from chillow.model.action import Action
from chillow.model.game import Game
from chillow.model.player import Player
from chillow.service.game_service import GameService


class PathfindingAI(ArtificialIntelligence):

    def __init__(self, player: Player, game: Game, max_speed):
        super().__init__(player)
        self.__game = game
        self.turn_ctr = 0
        self.__max_speed = max_speed

    def create_next_action(self, game: Game) -> Action:
        self.turn_ctr += 1
        self.__game = game
        game_service = GameService(game)
        game_service.turn.turn_ctr = self.turn_ctr

        surviving_actions = self.find_surviving_actions(game_service)

        return self.find_action_by_best_path_connection(surviving_actions) if len(
            surviving_actions) > 0 else Action.get_random_action()

    def find_action_by_best_path_connection(self, actions: List[Action]) -> Action:
        best_action: Tuple[Action, int] = (actions[0], 0)
        free_cells_for_pathfinding = self.get_different_free_cells_from_playground()
        grid = self.translate_cell_matrix_to_pathfinding_grid()

        path_finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        start = grid.node(self.player.x, self.player.y)
        for action in actions:
            current_possible_actions = 0
            for free_cell in free_cells_for_pathfinding:
                end = grid.node(free_cell[0], free_cell[1])
                path, runs = path_finder.find_path(start, end, grid)
                if runs > 0:
                    current_possible_actions += 1
            if len(best_action) == 0 or best_action[1] < current_possible_actions:
                best_action = (action, current_possible_actions)

        return best_action[0]

    def get_different_free_cells_from_playground(self) -> List[(int, int)]:
        # Todo: currently generating random points. Try generating equal distributed points
        free_cells: List[(int, int)] = []
        for i in range(20):
            x = randint(0, self.__game.width)
            y = randint(0, self.__game.height)
            if self.__game.cells[y][x].players is None or len(self.__game.cells[y][x].players) == 0:
                free_cells.append((x, y))
        return free_cells

    def translate_cell_matrix_to_pathfinding_grid(self) -> Grid:
        matrix = [[0 for _ in range(self.__game.width)] for _ in range(self.__game.height)]
        for i in range(len(self.__game.cells)):
            for j in range(len(self.__game.cells[i])):
                if self.__game.cells[i][j].players is not None and len(self.__game.cells[i][j].players) > 0:
                    matrix[i][j] = 1
        return Grid(matrix=matrix)
