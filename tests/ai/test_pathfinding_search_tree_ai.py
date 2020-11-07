import unittest

import tests
from chillow.ai.search_tree_pathfinding_ai import SearchTreePathfindingAI
from chillow.model.action import Action
from chillow.service.data_loader import JSONDataLoader


class PathfindingSearchTreeAITest(unittest.TestCase):

    def setUp(self):
        self.data_loader = JSONDataLoader()

    def test_should_select_action_to_let_player_survive_next_two_rounds(self):
        game = self.data_loader.load(tests.read_test_file("ai/game_4.json"))
        sut = SearchTreePathfindingAI(game.you, 3, 100, 2)

        result = sut.create_next_action(game)

        self.assertEqual(Action.turn_left, result)
