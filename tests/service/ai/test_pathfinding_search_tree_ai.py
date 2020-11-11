import unittest
from datetime import datetime

import tests
from chillow.model.action import Action
from chillow.service.ai.pathfinding_search_tree_ai import PathfindingSearchTreeAI
from chillow.model.cell import Cell
from chillow.model.direction import Direction
from chillow.model.game import Game
from chillow.model.player import Player
from chillow.service.data_loader import JSONDataLoader


class PathfindingSearchTreeAITest(unittest.TestCase):

    def setUp(self) -> None:
        player1 = Player(1, 0, 0, Direction.up, 1, True, "")
        player2 = Player(2, 0, 1, Direction.down, 3, True, "")
        players = [player1, player2]
        cells = [[Cell([player1]), Cell(), Cell(), Cell()],
                 [Cell([player2]), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell()]]

        self.game = Game(4, 4, cells, players, 2, True, datetime.now())
        self.sut = PathfindingSearchTreeAI(player1, 2, 100, 2, 0.75)
        self.data_loader = JSONDataLoader()

    def test_should_select_action_to_let_player_survive_next_two_rounds(self):
        game = self.data_loader.load(tests.read_test_file("ai/game_4.json"))
        result = self.sut.create_next_action(game)

        self.assertEqual(Action.turn_left, result)

    def test_get_best_action_should_find_best_action(self):
        action = self.sut.get_best_action([(Action.change_nothing, 10), (Action.speed_up, 8)], [Action.change_nothing])

        self.assertEqual(action, Action.change_nothing)

    def test_get_best_action_should_find_best_action_when_first_best_action_ist_not_in_search_tree_list(self):
        action = self.sut.get_best_action([(Action.change_nothing, 10), (Action.speed_up, 10)], [Action.speed_up])

        self.assertEqual(action, Action.speed_up)

    def test_get_best_action_should_find_best_action_with_tolerance(self):
        action = self.sut.get_best_action([(Action.change_nothing, 10), (Action.speed_up, 8)], [Action.speed_up])

        self.assertEqual(action, Action.speed_up)

    def test_get_best_pathfinding_action_when_no_tolerance_matches(self):
        action = self.sut.get_best_action([(Action.change_nothing, 10), (Action.speed_up, 8)], [Action.slow_down])

        self.assertEqual(action, Action.change_nothing)

    def test_get_best_pathfinding_action_return_None_when_lists_are_none(self):
        action = self.sut.get_best_action(None, None)

        self.assertIsNone(action)

    def test_get_best_pathfinding_action_return_none_when_lists_are_empty(self):
        action = self.sut.get_best_action([], [])

        self.assertIsNone(action)

    def test_get_best_pathfinding_action_return_search_tree_action_when_pathfinding_list_is_empty(self):
        action = self.sut.get_best_action([], [Action.speed_up])

        self.assertEqual(action, Action.speed_up)

    def test_get_best_pathfinding_action_return_when_search_tree_list_is_empty(self):
        action = self.sut.get_best_action([(Action.speed_up, 1)], [])

        self.assertEqual(action, Action.speed_up)
