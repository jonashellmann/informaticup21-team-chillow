import unittest
from datetime import datetime

from chillow.ai.pathfinding_ai import PathfindingAI
from chillow.model.cell import Cell
from chillow.model.direction import Direction
from chillow.model.game import Game
from chillow.model.player import Player


class PathfindingAITest(unittest.TestCase):

    def test_translate_cell_matrix_to_pathfinding_matrix_should_be_correct(self):
        player1 = Player(1, 0, 0, Direction.up, 1, True, "")
        player2 = Player(2, 0, 1, Direction.down, 3, True, "")
        players = [player1, player2]
        cells = [[Cell([player1]), Cell()],
                 [Cell([player2]), Cell()]]

        game = Game(2, 2, cells, players, 2, True, datetime.now())
        sut = PathfindingAI(player1, game, 2, 10)
        expected_matrix = [[0, 1],
                           [0, 1]]

        matrix = sut.translate_cell_matrix_to_pathfinding_matrix(game)

        self.assertEqual(matrix, expected_matrix)
