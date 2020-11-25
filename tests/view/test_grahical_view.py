import io
import unittest
from datetime import datetime
from unittest.mock import patch

from chillow.model.cell import Cell
from chillow.model.direction import Direction
from chillow.model.game import Game
from chillow.model.player import Player
from chillow.view.graphical_view import GraphicalView


class GraphicalViewTest(unittest.TestCase):


    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_correct_output_winner(self, mock_stdout):
        player1 = Player(1, 0, 0, Direction.up, 1, True, "p1")
        player2 = Player(2, 0, 1, Direction.down, 3, False, "")
        players = [player1, player2]
        cells = [[Cell([player1]), Cell(), Cell()],
                 [Cell([player2]), Cell(), Cell()],
                 [Cell(), Cell(), Cell()]]
        game = Game(3, 3, cells, players, 2, False, datetime.now())

        sut = GraphicalView()
        sut.update(game)

        self.assertTrue("Winner: Player 1 (p1). Your player ID was 2" in str(mock_stdout.getvalue()))

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_correct_output_no_winner(self, mock_stdout):
        player1 = Player(1, 0, 0, Direction.up, 1, False, "p1")
        player2 = Player(2, 0, 1, Direction.down, 3, False, "")
        players = [player1, player2]
        cells = [[Cell([player1]), Cell(), Cell()],
                 [Cell([player2]), Cell(), Cell()],
                 [Cell(), Cell(), Cell()]]
        game = Game(3, 3, cells, players, 2, False, datetime.now())

        sut = GraphicalView()
        sut.update(game)

        self.assertTrue("No winner in game." in str(mock_stdout.getvalue()))