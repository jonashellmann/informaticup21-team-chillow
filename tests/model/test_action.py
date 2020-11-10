import unittest

from chillow.model.action import Action


class ActionTest(unittest.TestCase):

    def test_should_have_five_different_actions(self):
        self.assertEqual(len(Action), 5)

    def test_get_actions_in_order(self):
        expected = []
        for action in list(Action):
            expected.append(action)

        result = Action.get_actions()

        self.assertEqual(expected, result)

    def test_get_actions_randomly(self):
        not_expected = []
        for action in list(Action):
            not_expected.append(action)

        result = Action.get_actions(True)
        while result == not_expected:
            result = Action.get_actions(True)

        self.assertNotEqual(not_expected, result)

    def test_get_random_action(self):
        not_expected = Action.get_random_action()

        result = Action.get_random_action()
        while not_expected == result:
            result = Action.get_random_action()

        self.assertNotEqual(not_expected, result)

    def test_create_combinations_as_product(self):
        player_count = 4

        result = Action.get_combinations(player_count)

        self.assertEqual(pow(len(Action), player_count), len(result))
        self.assertEqual(player_count, len(result[0]))
