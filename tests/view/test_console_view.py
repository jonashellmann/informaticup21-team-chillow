import unittest
from unittest.mock import patch

from chillow.model.action import Action
from chillow.view.console_view import ConsoleView


class ConsoleViewTest(unittest.TestCase):

    @patch('chillow.view.console_view.ConsoleView.get_input', return_value='u')
    def test_read_next_action_should_return_correct_action_input_u(self, input):
        sut = ConsoleView()

        self.assertTrue(sut.read_next_action(), Action.speed_up)

    @patch('chillow.view.console_view.ConsoleView.get_input', return_value='d')
    def test_read_next_action_should_return_correct_action_input_d(self, input):
        sut = ConsoleView()

        self.assertTrue(sut.read_next_action(), Action.slow_down)

    @patch('chillow.view.console_view.ConsoleView.get_input', return_value='r')
    def test_read_next_action_should_return_correct_action_input_r(self, input):
        sut = ConsoleView()

        self.assertTrue(sut.read_next_action(), Action.turn_right)


    @patch('chillow.view.console_view.ConsoleView.get_input', return_value='l')
    def test_read_next_action_should_return_correct_action_input_l(self, input):
        sut = ConsoleView()

        self.assertTrue(sut.read_next_action(), Action.turn_left)

    @patch('chillow.view.console_view.ConsoleView.get_input', return_value='n')
    def test_read_next_action_should_return_correct_action_input_n(self, input):
        sut = ConsoleView()

        self.assertTrue(sut.read_next_action(), Action.change_nothing)

    @patch('chillow.view.console_view.ConsoleView.get_input', return_value='wrong')
    def test_read_next_action_should_return_change_nothing_on_wrong_input(self, input):
        sut = ConsoleView()

        self.assertTrue(sut.read_next_action(), Action.change_nothing)