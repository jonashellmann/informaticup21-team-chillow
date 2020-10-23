import unittest

from src.main.python.model.direction import Direction


class DirectionTest(unittest.TestCase):

    def test_should_have_four_different_directions(self):
        self.assertEqual(len(Direction), 4)
