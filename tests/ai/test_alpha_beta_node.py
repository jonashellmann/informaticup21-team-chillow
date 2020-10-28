import unittest

from chillow.ai.alpha_beta_pruning_ai import AlphaBetaRoot, AlphaBetaNode
from chillow.model.action import Action
import tests
from chillow.service.data_loader import JSONDataLoader


class AlphaBetaPruningAITest(unittest.TestCase):

    def setUp(self):
        self.data_loader = JSONDataLoader()

    def test_node_return_correct_children_with_depth_one(self):
        testfile = open(tests.get_test_file_path("game_1.json"))
        game = self.data_loader.load(testfile.read())
        root = AlphaBetaRoot(game)

        result = root.get_children(0)

        self.assertEqual([root], result)
        testfile.close()

    def test_node_return_correct_children_with_depth_two(self):
        testfile = open(tests.get_test_file_path("game_1.json"))
        game = self.data_loader.load(testfile.read())
        root = AlphaBetaRoot(game)
        child1 = AlphaBetaNode(game, Action.turn_right)
        child2 = AlphaBetaNode(game, Action.turn_right)
        root.append_child(child1)
        root.append_child(child2)

        result = root.get_children(1)

        self.assertEqual([child1, child2], result)
        testfile.close()