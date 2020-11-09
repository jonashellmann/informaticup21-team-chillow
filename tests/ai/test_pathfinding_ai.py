import unittest
from datetime import datetime

from chillow.ai.pathfinding_ai import PathfindingAI
from chillow.model.action import Action
from chillow.model.cell import Cell
from chillow.model.direction import Direction
from chillow.model.game import Game
from chillow.model.player import Player


class PathfindingAITest(unittest.TestCase):

    def test_get_random_free_cells_from_playground_should_return_correct_number_of_free_cells(self):
        player1 = Player(1, 0, 0, Direction.up, 1, True, "")
        player2 = Player(2, 0, 1, Direction.down, 3, True, "")
        players = [player1, player2]
        cells = [[Cell([player1]), Cell(), Cell()],
                 [Cell([player2]), Cell(), Cell()],
                 [Cell(), Cell(), Cell()]]
        count_free_cells = 5
        game = Game(3, 3, cells, players, 2, True, datetime.now())
        sut = PathfindingAI(player1, 2, count_free_cells)

        free_cells_xy = sut.get_random_free_cells_from_playground(game)

        self.assertEqual(len(free_cells_xy), count_free_cells)
        for (x, y) in free_cells_xy:
            self.assertTrue(game.cells[y][x].players is None)

    def test_get_random_free_cells_from_playground_should_return_correct_number_of_free_cells_in_late_game(self):
        player1 = Player(1, 0, 0, Direction.up, 1, True, "")
        player2 = Player(2, 0, 1, Direction.down, 3, True, "")
        players = [player1, player2]
        cells = [[Cell([player1]),  Cell(), Cell()],
                 [Cell([player2]),  Cell(), Cell()],
                 [Cell(),           Cell(), Cell()]]
        count_free_cells = 100  # Not possible. The maximum possible free cells should be returned
        max_possible_free_cells = 7
        game = Game(3, 3, cells, players, 2, True, datetime.now())
        sut = PathfindingAI(player1, 2, count_free_cells)

        free_cells_xy = sut.get_random_free_cells_from_playground(game)

        self.assertEqual(len(free_cells_xy), max_possible_free_cells)
        for (x, y) in free_cells_xy:
            self.assertTrue(game.cells[y][x].players is None)

    def test_create_action_should_return_only_possible_action(self):
        player1 = Player(1, 0, 0, Direction.up, 1, True, "")
        player2 = Player(2, 0, 1, Direction.down, 3, True, "")
        players = [player1, player2]
        cells = [[Cell([player1]),  Cell(), Cell()],
                 [Cell([player2]),  Cell(), Cell()],
                 [Cell(),           Cell(), Cell()]]
        game = Game(3, 3, cells, players, 2, True, datetime.now())
        sut = PathfindingAI(player1, 2, 10)

        action = sut.create_next_action(game)

        self.assertEqual(action, Action.turn_right)

    def test_create_action_should_return_action_with_best_connection(self):
        player1 = Player(1, 0, 0, Direction.down, 1, True, "")
        player2 = Player(2, 0, 2, Direction.down, 3, True, "")
        players = [player1, player2]
        cells = [[Cell([player1]),  Cell(),             Cell()],
                 [Cell(),           Cell([player2]),    Cell()],
                 [Cell([player2]),  Cell(),             Cell()]]
        game = Game(3, 3, cells, players, 2, True, datetime.now())
        sut = PathfindingAI(player1, 2, 10)

        action = sut.create_next_action(game)

        self.assertEqual(action, Action.turn_left)

    def test_create_action_should_return_one_of_the_possible_action_with_best_connection(self):
        player1 = Player(1, 0, 0, Direction.right, 2, True, "")
        player2 = Player(2, 0, 2, Direction.down, 3, True, "")
        players = [player1, player2]
        cells = [[Cell([player1]),  Cell(),             Cell()],
                 [Cell(),           Cell([player2]),    Cell()],
                 [Cell([player2]),  Cell(),             Cell()]]
        game = Game(3, 3, cells, players, 2, True, datetime.now())
        sut = PathfindingAI(player1, 2, 10)

        actions = sut.find_actions_by_best_path_connection([Action.change_nothing, Action.slow_down], game)

        self.assertEqual(actions[0][0], Action.slow_down)

    def test_create_action_should_return_None_if_given_action_list_is_none(self):
        player1 = Player(1, 0, 0, Direction.right, 2, True, "")
        player2 = Player(2, 0, 2, Direction.down, 3, True, "")
        players = [player1, player2]
        cells = [[Cell([player1]),  Cell(),             Cell()],
                 [Cell(),           Cell([player2]),    Cell()],
                 [Cell([player2]),  Cell(),             Cell()]]
        game = Game(3, 3, cells, players, 2, True, datetime.now())
        sut = PathfindingAI(player1, 2, 10)

        actions = sut.find_actions_by_best_path_connection(None, game)

        self.assertIsNone(actions)

    def test_create_action_should_return_None_if_given_action_list_is_empty(self):
        player1 = Player(1, 0, 0, Direction.right, 2, True, "")
        player2 = Player(2, 0, 2, Direction.down, 3, True, "")
        players = [player1, player2]
        cells = [[Cell([player1]),  Cell(),             Cell()],
                 [Cell(),           Cell([player2]),    Cell()],
                 [Cell([player2]),  Cell(),             Cell()]]
        game = Game(3, 3, cells, players, 2, True, datetime.now())
        sut = PathfindingAI(player1, 2, 10)

        actions = sut.find_actions_by_best_path_connection([], game)

        self.assertIsNone(actions)
