import unittest

from datetime import datetime, timezone

from chillow.model.game import Game
from chillow.model.player import Player
from chillow.model.cell import Cell
from chillow.model.direction import Direction
from chillow.service.data_loader import JSONDataLoader
import tests


class JSONDataWriterTest(unittest.TestCase):

    def setUp(self):
        self.sut = JSONDataLoader()

    def test_convert_json_to_running_game(self):
        json = tests.read_test_file("service/game.json")
        player1 = Player(1, 2, 2, Direction.up, 1, True, "")
        player2 = Player(2, 1, 0, Direction.down, 3, True, "")
        player3 = Player(3, 4, 3, Direction.left, 2, False, "Name 3")
        players = [player1, player2, player3]
        cells = [
            [Cell(), Cell([player2]), Cell(), Cell(), Cell()],
            [Cell(), Cell(), Cell(), Cell(), Cell()],
            [Cell(), Cell([player1]), Cell([player1]), Cell(), Cell()],
            [Cell(), Cell(), Cell(), Cell(), Cell([player3])]
        ]
        time = datetime(2020, 10, 1, 12, 5, 13, 0, timezone.utc)
        expected = Game(5, 4, cells, players, 2, True, time)

        result = self.sut.load(json)

        self.assertEqual(expected, result)

    def test_convert_json_to_ended_game(self):
        json = tests.read_test_file("service/game_ended.json")
        player1 = Player(1, 2, 2, Direction.up, 1, True, "")
        player2 = Player(2, 1, 0, Direction.down, 3, True, "")
        player3 = Player(3, 4, 3, Direction.left, 2, False, "Name 3")
        players = [player1, player2, player3]
        cells = [
            [Cell(), Cell([player2]), Cell(), Cell(), Cell()],
            [Cell(), Cell(), Cell(), Cell(), Cell()],
            [Cell(), Cell([player1]), Cell([player1]), Cell(), Cell()],
            [Cell(), Cell(), Cell(), Cell(), Cell([player3])]
        ]
        expected = Game(5, 4, cells, players, 2, False)

        result = self.sut.load(json)

        self.assertEqual(expected, result)
