import unittest
from datetime import datetime, timezone

from chillow.game_services.game_service import GameService
from chillow.model.action import Action
from chillow.model.cell import Cell
from chillow.model.direction import Direction
from chillow.model.game import Game
from chillow.model.player import Player


class TurnTest(unittest.TestCase):

    def setUp(self):
        self.player1 = Player(1, 2, 2, Direction.up, 1, True, "")
        self.player2 = Player(2, 1, 0, Direction.down, 3, True, "")
        self.player3 = Player(3, 4, 3, Direction.left, 2, False, "Name 3")
        players = [self.player1, self.player2, self.player3]
        cells = [[Cell() for i in range(40)] for j in range(40)]
        cells[10][10] = Cell([self.player1])
        cells[10][30] = Cell([self.player2])
        cells[30][10] = Cell([self.player3])
        time = datetime(2020, 10, 1, 12, 5, 13, 0, timezone.utc)
        self.game = Game(5, 4, cells, players, 2, True, time)
        self.sut = GameService(self.game)

    def test_game_should_end_when_less_than_two_players_are_left(self):
        self.player1.active = False
        self.player2.active = False

        self.assertEqual(self.sut.is_game_ended(), True)

    def test_game_should_not_end_when_more_than_one_players_are_left(self):
        self.player1.active = False

        self.assertEqual(self.sut.is_game_ended(), True)

    def test_player_should_loose_if_he_did_more_than_one_action_in_one_round(self):
        self.sut.do_action(self.player1, Action.speed_up)
        self.sut.do_action(self.player1, Action.speed_up)

        self.assertEqual(self.player1.active, False)

    def test_player_should_not_loose_if_he_did_exactly_one_action_in_one_round(self):
        self.sut.do_action(self.player1, Action.speed_up)

        self.assertEqual(self.player1.active, False)

    def test_player_should_loose_if_he_exceeded_time_limit(self):
        pass
