import unittest

from chillow.game_services.turn import Turn
import chillow.game_services.exceptions as ex
from datetime import datetime
from datetime import timedelta

from chillow.model.direction import Direction
from chillow.model.player import Player


class TurnTest(unittest.TestCase):

    def setUp(self):
        self.player1 = Player(1, 2, 2, Direction.up, 1, True, "")
        self.player2 = Player(2, 1, 0, Direction.down, 3, True, "")
        self.players = [self.player1, self.player2]
        date = datetime.now() + timedelta(0, 180)
        self.sut = Turn(self.players, date)

    def test_turn_not_ended(self):
        self.assertEqual(self.sut.action(self.player1), False)

    def test_turn_should_be_ended(self):
        self.sut.action(self.player1)

        self.assertEquals(self.sut.action(self.player2), True)

    def test_player_should_not_be_able_to_do_multiple_Actions_in_one_turn(self):
        self.sut.action(self.player1)

        with self.assertRaises(ex.MultipleActionByPlayerError): self.sut.action(self.player1)

    def test_deadlineException(self):
        date = datetime.now() - timedelta(0, 180)
        self.sut = Turn(self.players, date)

        with self.assertRaises(ex.DeadLineExceededException): self.sut.action(self.player1)

    def test_new_turn_should_be_initialized(self):
        self.sut.action(self.player1)
        self.sut.action(self.player2)

        self.assertEquals(len(self.sut.playersWithPendingAction), len(self.sut.players))

    def test_inactive_players_should_not_be_added_to_pending_actions(self):
        self.player1.active = False
        self.sut.action(self.player1)
        self.sut.action(self.player2)

        self.assertEquals(len(self.sut.playersWithPendingAction), len(self.sut.players) - 1)