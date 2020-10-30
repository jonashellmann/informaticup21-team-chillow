import unittest

from chillow.ai.search_tree_ai import SearchTreeAI
from chillow.model.action import Action
import tests
from chillow.service.data_loader import JSONDataLoader


class SearchTreeAITest(unittest.TestCase):

    def setUp(self):
        self.data_loader = JSONDataLoader()

    def test_should_select_action_to_let_player_survive_next_round(self):
        game = self.data_loader.load(tests.read_test_file("game_1.json"))
        sut = SearchTreeAI(game.you, 1)

        result = sut.create_next_action(game)

        self.assertEqual(Action.turn_right, result)

    def test_should_select_action_to_let_player_survive_next_two_rounds(self):
        game = self.data_loader.load(tests.read_test_file("game_2.json"))
        sut = SearchTreeAI(game.you, 2)

        result = sut.create_next_action(game)

        self.assertEqual(Action.turn_right, result)
