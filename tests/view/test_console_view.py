import io
import unittest
from datetime import datetime
from unittest.mock import patch


from chillow.model.action import Action
from chillow.model.cell import Cell
from chillow.model.direction import Direction
from chillow.model.game import Game
from chillow.model.player import Player
from chillow.view.console_view import ConsoleView


class ConsoleViewTest(unittest.TestCase):

    def setUp(self) -> None:
        self.sut = ConsoleView()

    @patch('chillow.view.console_view.ConsoleView.get_input', return_value='u')
    def test_read_next_action_should_return_correct_action_input_u(self, _):
        self.assertTrue(self.sut.read_next_action(), Action.speed_up)

    @patch('chillow.view.console_view.ConsoleView.get_input', return_value='d')
    def test_read_next_action_should_return_correct_action_input_d(self, _):
        self.assertTrue(self.sut.read_next_action(), Action.slow_down)

    @patch('chillow.view.console_view.ConsoleView.get_input', return_value='r')
    def test_read_next_action_should_return_correct_action_input_r(self, _):
        self.assertTrue(self.sut.read_next_action(), Action.turn_right)

    @patch('chillow.view.console_view.ConsoleView.get_input', return_value='l')
    def test_read_next_action_should_return_correct_action_input_l(self, _):
        self.assertTrue(self.sut.read_next_action(), Action.turn_left)

    @patch('chillow.view.console_view.ConsoleView.get_input', return_value='n')
    def test_read_next_action_should_return_correct_action_input_n(self, _):
        self.assertTrue(self.sut.read_next_action(), Action.change_nothing)

    @patch('chillow.view.console_view.ConsoleView.get_input', return_value='wrong')
    def test_read_next_action_should_return_change_nothing_on_wrong_input(self, _):
        self.assertTrue(self.sut.read_next_action(), Action.change_nothing)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_correct_output_on_end(self,  mock_stdout):
        self.sut.end()
        self.assertTrue("Game ended!" in str(mock_stdout.getvalue()))

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_correct_output_round_1(self,  mock_stdout):
        player1 = Player(1, 0, 0, Direction.up, 1, True, "p1")
        player2 = Player(2, 0, 1, Direction.down, 3, True, "")
        cells = [[Cell([player1])],
                 [Cell([player2])]]
        game = Game(1, 2, cells, [player1, player2], 2, True, datetime.now())

        self.sut.update(game)
        self.assertTrue("Round :  0" in str(mock_stdout.getvalue()))

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_correct_output_round_2(self,  mock_stdout):
        player1 = Player(1, 0, 0, Direction.up, 1, True, "p1")
        player2 = Player(2, 0, 1, Direction.down, 3, True, "")
        cells = [[Cell([player1]), Cell([player1])],
                 [Cell([player2]), Cell()]]
        game = Game(2, 2, cells, [player1, player2], 2, True, datetime.now())

        self.sut.update(game)
        self.sut.update(game)

        self.assertTrue("Round :  0" in str(mock_stdout.getvalue()))
        self.assertTrue("Round :  1" in str(mock_stdout.getvalue()))

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_correct_output_winner(self, mock_stdout):
        player1 = Player(1, 0, 0, Direction.up, 1, True, "p1")
        player2 = Player(2, 0, 1, Direction.down, 3, False, "")
        cells = [[Cell([player1])],
                 [Cell([player2])]]
        game = Game(1, 2, cells, [player1, player2], 2, False, datetime.now())
        self.sut.update(game)

        self.assertTrue("Winner: Player 1 (p1). Your player ID was 2" in str(mock_stdout.getvalue()))

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_correct_output_no_winner(self, mock_stdout):
        player1 = Player(1, 0, 0, Direction.up, 1, False, "p1")
        player2 = Player(2, 0, 1, Direction.down, 3, False, "")
        cells = [[Cell([player1])],
                 [Cell([player2])]]
        game = Game(1, 2, cells, [player1, player2], 2, False, datetime.now())
        self.sut.update(game)

        self.assertTrue("No winner in game." in str(mock_stdout.getvalue()))
