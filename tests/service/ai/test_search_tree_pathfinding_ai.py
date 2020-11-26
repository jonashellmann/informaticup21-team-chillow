import unittest
from multiprocessing import Value

import tests
from chillow.service.ai.search_tree_pathfinding_ai import SearchTreePathfindingAI
from chillow.model.action import Action
from chillow.service.data_loader import JSONDataLoader


class SearchTreePathfindingAITest(unittest.TestCase):

    def setUp(self):
        self.data_loader = JSONDataLoader()

    def test_should_select_action_to_let_player_survive_next_two_rounds(self):
        game = self.data_loader.load(tests.read_test_file("ai/game_4.json"))
        sut = SearchTreePathfindingAI(game.you, 3, 100, 2)

        result = Value('i')
        sut.create_next_action(game, result)

        self.assertEqual(Action.turn_left, Action.get_by_index(result.value))

    def test_should_select_action_of_pathfinding_ai_if_surviving_next_two_rounds_is_not_possible(self):
        game = self.data_loader.load(tests.read_test_file("ai/game_5.json"))
        sut = SearchTreePathfindingAI(game.you, 3, 50, 10)

        result = Value('i')
        sut.create_next_action(game, result)

        self.assertEqual(Action.turn_right, Action.get_by_index(result.value))

    def test_should_select_default_action(self):
        game = self.data_loader.load(tests.read_test_file("ai/game_6.json"))
        sut = SearchTreePathfindingAI(game.you, 3, 50, 10)

        result = Value('i')
        sut.create_next_action(game, result)

        self.assertEqual(Action.get_default(), Action.get_by_index(result.value))


    def test_get_information(self):
        game = self.data_loader.load(tests.read_test_file("ai/game_4.json"))
        sut = SearchTreePathfindingAI(game.you, 3, 100, 2, 5)
        expected = "max_speed=3, count_paths_to_check=100, depth=2, distance_to_check=5"

        result = sut.get_information()

        self.assertEqual(expected, result)
