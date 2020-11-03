import unittest

import tests
from chillow.ai.pathfinding_search_tree_ai import PathfindingSearchTreeAI
from chillow.model.action import Action
from chillow.service.data_loader import JSONDataLoader


class PathfindingSearchTreeAITest(unittest.TestCase):

    def setUp(self):
        self.data_loader = JSONDataLoader()

    def test_should_select_action_to_let_player_survive_next_two_rounds_1(self):
        game = self.data_loader.load(tests.read_test_file("ai/game_2.json"))
        sut = PathfindingSearchTreeAI(game.you, 3, 20, 2)

        result = sut.create_next_action(game)

        self.assertEqual(Action.turn_right, result)

    def test_should_select_action_to_let_player_survive_next_two_rounds_2(self):
        game = self.data_loader.load(tests.read_test_file("ai/game_3.json"))
        sut = PathfindingSearchTreeAI(game.you, 3, 20, 2)

        result = sut.create_next_action(game)

        self.assertEqual(Action.slow_down, result)
