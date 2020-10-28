import unittest

from chillow.ai.alpha_beta_pruning_ai import AlphaBetaPruningAI
from chillow.model.action import Action
import tests
from chillow.service.data_loader import JSONDataLoader


class AlphaBetaPruningAITest(unittest.TestCase):

    def setUp(self):
        self.data_loader = JSONDataLoader()

    def test_should_select_action_to_let_player_survive_next_round(self):
        testfile = open(tests.get_test_file_path("game_1.json"))
        game = self.data_loader.load(testfile.read())
        sut = AlphaBetaPruningAI(game.you, 1)

        result = sut.create_next_action(game)

        self.assertEquals(result, Action.turn_right)
        testfile.close()