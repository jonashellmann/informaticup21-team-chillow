import unittest

from chillow.model.action import Action


class ActionTest(unittest.TestCase):

    def test_should_have_five_different_actions(self):
        self.assertEqual(len(Action), 5)
