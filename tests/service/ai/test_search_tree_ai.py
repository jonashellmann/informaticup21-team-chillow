import unittest

from chillow.service.ai.return_value import ReturnValue
from chillow.service.ai.search_tree_ai import SearchTreeAI
from chillow.model.action import Action
import tests
from chillow.service.data_loader import JSONDataLoader


class SearchTreeAITest(unittest.TestCase):

    def setUp(self):
        self.data_loader = JSONDataLoader()

    def test_should_select_action_to_let_player_survive_next_round(self):
        game = self.data_loader.load(tests.read_test_file("ai/game_1.json"))
        sut = SearchTreeAI(game.you, 1, 3, True)

        result = ReturnValue()
        sut.create_next_action(game, result)

        self.assertEqual(Action.turn_right, result.action)

    def test_should_select_action_to_let_player_survive_next_two_rounds_1(self):
        game = self.data_loader.load(tests.read_test_file("ai/game_2.json"))
        sut = SearchTreeAI(game.you, 2)

        result = ReturnValue()
        sut.create_next_action(game, result)

        self.assertEqual(Action.turn_right, result.action)

    def test_should_select_action_to_let_player_survive_next_two_rounds_2(self):
        game = self.data_loader.load(tests.read_test_file("ai/game_3.json"))
        sut = SearchTreeAI(game.you, 2, 2)

        result = ReturnValue()
        sut.create_next_action(game, result)

        self.assertEqual(Action.slow_down, result.action)

    def test_get_information(self):
        game = self.data_loader.load(tests.read_test_file("ai/game_3.json"))
        sut = SearchTreeAI(game.you, 2, 3, True, 10)
        expected = "max_speed=3, depth=2, randomize=True, distance_to_check=10"

        result = sut.get_information()

        self.assertEqual(expected, result)
