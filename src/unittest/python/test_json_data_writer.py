import unittest

from src.main.python.data_writer import JSONDataWriter
from src.main.python.model.action import Action


class JSONDataWriterTest(unittest.TestCase):

    def test_action_should_be_represented_in_json(self):
        data_writer = JSONDataWriter()
        action = Action.speed_up

        result = data_writer.write(action)

        self.assertEqual(result, '{"action": "speed_up"}')
