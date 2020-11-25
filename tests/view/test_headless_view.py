import unittest
from datetime import datetime

from chillow.model.cell import Cell
from chillow.model.direction import Direction
from chillow.model.game import Game
from chillow.model.player import Player
from chillow.view.headless_view import HeadlessView


class HeadlessViewTest(unittest.TestCase):

    def setUp(self) -> None:
        self.sut = HeadlessView()

    def test_update(self):
        player1 = Player(1, 0, 0, Direction.up, 1, True, "p1")
        player2 = Player(2, 0, 1, Direction.down, 3, False, "")
        cells = [[Cell([player1])],
                 [Cell([player2])]]
        game = Game(1, 2, cells, [player1, player2], 2, False, datetime.now())
        self.sut.update(game)

    def test_end(self):
        self.sut.end()

    def test_read_next_action(self):
        self.sut.read_next_action()
