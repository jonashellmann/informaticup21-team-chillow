import io
import unittest
from datetime import datetime
from unittest.mock import Mock, ANY, call, patch

from chillow.model.action import Action
from chillow.model.cell import Cell
from chillow.model.direction import Direction
from chillow.model.game import Game
from chillow.model.player import Player
from chillow.view.graphical_view import GraphicalView

pygame_mock = Mock()


class GraphicalViewTest(unittest.TestCase):

    def setUp(self) -> None:
        self.sut = GraphicalView(pygame_mock)

        mock_event = Mock()
        mock_event.type = pygame_mock.KEYDOWN = 1
        pygame_mock.event.get.return_value = [mock_event]
        pygame_mock.K_UP = 0
        pygame_mock.K_DOWN = 1
        pygame_mock.K_RIGHT = 2
        pygame_mock.K_LEFT = 3
        pygame_mock.K_SPACE = 4
        pygame_mock.key.get_pressed.return_value = [False for _ in range(pygame_mock.K_SPACE + 1)]

    def test_draws_all_players_correctly(self):
        player1 = Player(1, 0, 0, Direction.up, 1, True, "p1")
        player2 = Player(2, 0, 1, Direction.down, 3, True, "")
        cells = [[Cell([player1]), Cell([player1])],
                 [Cell([player2]), Cell()]]
        game = Game(2, 2, cells, [player1, player2], 2, True, datetime.now())
        expected_calls = [
            call(ANY, (255, 61, 0), (0, 0, 10, 10)),
            call(ANY, (0, 0, 0), (2, 2, 6, 6)),
            call(ANY, (255, 61, 0), (11, 0, 10, 10)),
            call(ANY, (156, 204, 101), (0, 11, 10, 10)),
            call(ANY, (0, 0, 0), (4, 15, 2, 2)),
            call(ANY, (0, 0, 0), (11, 11, 10, 10))
        ]

        self.sut.update(game)

        pygame_mock.init.assert_called_once()
        pygame_mock.draw.rect.assert_has_calls(expected_calls, any_order=False)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_draws_all_players_correctly_in_ended_game_no_winner(self, mock_stdout):
        player1 = Player(1, 0, 0, Direction.up, 1, False, "p1")
        player2 = Player(2, 0, 1, Direction.down, 3, False, "")
        cells = [[Cell([player1]), Cell([player1])],
                 [Cell([player2]), Cell()]]
        game = Game(2, 2, cells, [player1, player2], 2, False, datetime.now())

        self.sut.update(game)

        self.assertTrue("No winner in game." in str(mock_stdout.getvalue()))

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_draws_all_players_correctly_in_ended_game_with_winner(self, mock_stdout):
        player1 = Player(1, 1, 0, Direction.up, 1, True, "Jonas")
        player2 = Player(2, 0, 1, Direction.down, 3, False, "Florian")
        cells = [[Cell(), Cell([player1])],
                 [Cell([player2]), Cell()]]
        game = Game(2, 2, cells, [player1, player2], 2, False, datetime.now())

        self.sut.update(game)

        self.assertTrue("Winner: Player 1 (Jonas). Your player ID was 2." in str(mock_stdout.getvalue()))

    @patch('sys.exit')
    @patch('time.sleep')
    def test_end_view(self, sys_exit, time_sleep):
        self.sut.end()

        pygame_mock.display.quit.assert_called_once()
        pygame_mock.quit.assert_called_once()

    def test_read_next_action_should_return_correct_action_input_up(self):
        pygame_mock.key.get_pressed.return_value[pygame_mock.K_UP] = True

        self.assertEqual(Action.speed_up, self.sut.read_next_action())

    def test_read_next_action_should_return_correct_action_input_down(self):
        pygame_mock.key.get_pressed.return_value[pygame_mock.K_DOWN] = True

        self.assertEqual(Action.slow_down, self.sut.read_next_action())

    def test_read_next_action_should_return_correct_action_input_right(self):
        pygame_mock.key.get_pressed.return_value[pygame_mock.K_RIGHT] = True

        self.assertEqual(Action.turn_right, self.sut.read_next_action())

    def test_read_next_action_should_return_correct_action_input_left(self):
        pygame_mock.key.get_pressed.return_value[pygame_mock.K_LEFT] = True

        self.assertEqual(Action.turn_left, self.sut.read_next_action())

    def test_read_next_action_should_return_correct_action_input_space(self):
        pygame_mock.key.get_pressed.return_value[pygame_mock.K_SPACE] = True

        self.assertEqual(Action.change_nothing, self.sut.read_next_action())

    @patch('sys.exit')
    @patch('time.sleep')
    def test_read_next_action_should_return_correct_action_input_close(self, sys_exit, time_sleep):
        mock_event = Mock()
        mock_event.type = pygame_mock.QUIT = 2
        pygame_mock.event.get.return_value = [mock_event]

        result = self.sut.read_next_action()

        self.assertEqual(Action.get_default(), result)
        pygame_mock.display.quit.assert_called()
        pygame_mock.quit.assert_called()
