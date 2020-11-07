import unittest
from datetime import datetime


from chillow.model.action import Action
from chillow.ai.pathfinding_search_tree_ai import PathfindingSearchTreeAI
from chillow.model.cell import Cell
from chillow.model.direction import Direction
from chillow.model.game import Game
from chillow.model.player import Player


class PathfindingSearchTreeAITest(unittest.TestCase):

    def setUp(self) -> None:
        player1 = Player(1, 0, 0, Direction.up, 1, True, "")
        player2 = Player(2, 0, 1, Direction.down, 3, True, "")
        players = [player1, player2]
        cells = [[Cell([player1]), Cell(), Cell(), Cell()],
                 [Cell([player2]), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell()]]

        game = Game(4, 4, cells, players, 2, True, datetime.now())
        self.sut = PathfindingSearchTreeAI(player1, 2, 10, 2, 0.75)

    def test_get_best_action_should_find_best_action(self):
        action = self.sut.get_best_action([(Action.change_nothing, 10), (Action.speed_up, 8)], [Action.change_nothing])

        self.assertEqual(action, Action.change_nothing)

    def test_get_best_action_shoud_find_best_action_when_first_best_action_ist_not_in_search_tree_list(self):
        action = self.sut.get_best_action([(Action.change_nothing, 10), (Action.speed_up, 10)], [Action.speed_up])

        self.assertEqual(action, Action.speed_up)

    def test_get_best_action_shoud_find_best_action_with_tolerance(self):
        action = self.sut.get_best_action([(Action.change_nothing, 10), (Action.speed_up, 8)], [Action.speed_up])

        self.assertEqual(action, Action.speed_up)

    def test_get_best_pathfinding_action_when_no_tolerance_matches(self):
        action = self.sut.get_best_action([(Action.change_nothing, 10), (Action.speed_up, 8)], [Action.slow_down])

        self.assertEqual(action, Action.change_nothing)
