import unittest
from datetime import datetime

from src.main.python.model.cell import Cell
from src.main.python.model.direction import Direction
from src.main.python.model.game import Game
from src.main.python.model.player import Player


class GameTest(unittest.TestCase):

    def test_examines_your_player_after_creation(self):
        cells = [[Cell(), Cell()], [Cell(), Cell()]]
        player = Player("2", 0, 0, Direction.up, 0, True, "Name 2")
        players = [
            Player("1", 0, 0, Direction.up, 0, True, "Name 1"),
            player,
            Player("3", 0, 0, Direction.up, 0, True, "Name 3")
        ]
        game = Game(2, 2, cells, players, 2, True, datetime.now())

        self.assertEqual(game.you, player)

    def test_raise_exception_on_non_existing_own_player(self):
        cells = [[Cell(), Cell()], [Cell(), Cell()]]
        players = [
            Player("1", 0, 0, Direction.up, 0, True, "Name 1"),
            Player("3", 0, 0, Direction.up, 0, True, "Name 3")
        ]

        with self.assertRaises(AttributeError):
            Game(2, 2, cells, players, 2, True, datetime.now())

    def test_raise_exception_on_wrong_width(self):
        cells = [
            [
                Cell()
            ],
            [
                Cell(), Cell()
            ]
        ]

        with self.assertRaises(AttributeError):
            Game(2, 2, cells, [], 0, True, datetime.now())

    def test_raise_exception_on_wrong_height(self):
        cells = [
            [
                Cell(), Cell()
            ]
        ]

        with self.assertRaises(AttributeError):
            Game(2, 2, cells, [], 0, True, datetime.now())
