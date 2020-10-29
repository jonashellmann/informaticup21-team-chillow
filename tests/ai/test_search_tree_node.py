import unittest

from chillow.service.data_loader import JSONDataLoader


# Todo: Weitere Tests schreiben
class AlphaBetaPruningAITest(unittest.TestCase):

    def setUp(self):
        self.data_loader = JSONDataLoader()
