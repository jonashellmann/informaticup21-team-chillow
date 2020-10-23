import unittest

from chillow.data_writer import JSONDataWriter
from chillow.model.action import Action


class JSONDataWriterTest(unittest.TestCase):

    def setUp(self):
        self.sut = JSONDataWriter()

    def test_action_should_be_represented_in_json(self):
        action = Action.speed_up

        result = self.sut.write(action)

        self.assertEqual(result, '{"action": "speed_up"}')
