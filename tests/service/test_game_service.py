import unittest
from datetime import datetime, timezone

from chillow.exceptions import PlayerOutsidePlaygroundException
from chillow.service.game_service import GameService
from chillow.model.action import Action
from chillow.model.cell import Cell
from chillow.model.direction import Direction
from chillow.model.game import Game
from chillow.model.player import Player


class GameTest(unittest.TestCase):

    def setUp(self):
        self.player1 = Player(1, 10, 10, Direction.down, 1, True, "")
        self.player2 = Player(2, 10, 30, Direction.down, 3, True, "")
        self.player3 = Player(3, 30, 10, Direction.right, 2, True, "Name 3")
        players = [self.player1, self.player2, self.player3]
        cells = [[Cell() for _ in range(40)] for _ in range(40)]
        cells[self.player1.y][self.player1.x] = Cell([self.player1])
        cells[self.player2.y][self.player2.x] = Cell([self.player2])
        cells[self.player3.y][self.player3.x] = Cell([self.player3])
        time = datetime(2020, 10, 1, 12, 5, 13, 0, timezone.utc)
        self.game = Game(40, 40, cells, players, 2, True, time)
        self.sut = GameService(self.game)

    def test_game_should_end_when_less_than_two_players_are_left(self):
        self.player1.active = False
        self.player2.active = False

        self.assertEqual(self.sut.is_game_running(), False)

    def test_game_should_not_end_when_more_than_one_players_are_left(self):
        self.player1.active = False

        self.assertEqual(self.sut.is_game_running(), True)

    def test_player_should_loose_if_he_did_more_than_one_action_in_one_round(self):
        self.sut.do_action(self.player1, Action.speed_up)
        self.sut.do_action(self.player1, Action.speed_up)

        self.assertEqual(self.player1.active, False)

    def test_player_should_not_loose_if_he_did_exactly_one_action_in_one_round(self):
        self.sut.do_action(self.player1, Action.speed_up)

        self.assertEqual(self.player1.active, True)

    def test_visited_cells_should_be_calculated_correctly_turn_1_to_5(self):
        self.player1.direction = Direction.down
        self.player1.speed = 1
        player1_x = self.player1.x
        player1_y = self.player1.y
        self.game.cells[self.player1.y][self.player1.x] = Cell([self.player1])
        self.player2.direction = Direction.up
        self.player2.speed = 3
        player2_x = self.player2.x
        player2_y = self.player2.y
        self.game.cells[self.player2.y][self.player2.x] = Cell([self.player2])
        self.player3.direction = Direction.down
        self.player3.speed = 5
        player3_x = self.player3.x
        player3_y = self.player3.y
        self.game.cells[self.player3.y][self.player3.x] = Cell([self.player3])
        visited_cells_p1_expected = [(player1_x, player1_y + 1), (player1_x, player1_y + 2)]
        visited_cells_p2_expected = [(player2_x, player2_y - 1), (player2_x, player2_y - 2)]
        visited_cells_p3_expected = [(player3_x + 1, player3_y), (player3_x + 2, player3_y), (player3_x + 3, player3_y),
                                     (player3_x + 4, player3_y), (player3_x + 5, player3_y)]

        visited_cells_p1 = self.sut.get_and_visit_cells(self.player1, Action.speed_up)
        visited_cells_p2 = self.sut.get_and_visit_cells(self.player2, Action.slow_down)
        visited_cells_p3 = self.sut.get_and_visit_cells(self.player3, Action.turn_left)

        self.assertEqual(visited_cells_p1_expected, visited_cells_p1)
        self.assertEqual(visited_cells_p2_expected, visited_cells_p2)
        self.assertEqual(visited_cells_p3_expected, visited_cells_p3)
        self.assertTrue(self.player1 in self.game.cells[player1_y + 1][player1_x].players)
        self.assertTrue(self.player1 in self.game.cells[player1_y + 2][player1_x].players)
        self.assertTrue(self.player2 in self.game.cells[player2_y - 2][player2_x].players)
        self.assertTrue(self.player2 in self.game.cells[player2_y - 2][player2_x].players)
        self.assertTrue(self.player3 in self.game.cells[player3_y][player3_x + 1].players)
        self.assertTrue(self.player3 in self.game.cells[player3_y][player3_x + 2].players)
        self.assertTrue(self.player3 in self.game.cells[player3_y][player3_x + 3].players)
        self.assertTrue(self.player3 in self.game.cells[player3_y][player3_x + 4].players)
        self.assertTrue(self.player3 in self.game.cells[player3_y][player3_x + 5].players)

    def test_visited_cells_should_be_calculated_correctly_turn_6(self):
        self.sut.turn.turn_ctr = 12  # 6, 12, 18 should all work
        self.player1.direction = Direction.down
        self.player1.speed = 1
        player1_x = self.player1.x
        player1_y = self.player1.y
        self.game.cells[10][10] = Cell([self.player1])
        self.player2.direction = Direction.up
        self.player2.speed = 5
        player2_x = self.player2.x
        player2_y = self.player2.y
        self.game.cells[10][30] = Cell([self.player2])
        visited_cells_p1_expected = [(player1_x, player1_y + 1), (player1_x, player1_y + 2)]
        visited_cells_p2_expected = [(player2_x, player2_y - 1), (player2_x, player2_y - 6)]

        visited_cells_p1 = self.sut.get_and_visit_cells(self.player1, Action.speed_up)
        visited_cells_p2 = self.sut.get_and_visit_cells(self.player2, Action.speed_up)

        self.assertEqual(visited_cells_p1_expected, visited_cells_p1)
        self.assertEqual(visited_cells_p2_expected, visited_cells_p2)
        self.assertTrue(self.player1 in self.game.cells[player1_y + 1][player1_x].players)
        self.assertTrue(self.player1 in self.game.cells[player1_y + 2][player1_x].players)
        self.assertTrue(self.player2 in self.game.cells[player2_y - 1][player2_x].players)
        self.assertTrue(self.player2 in self.game.cells[player2_y - 6][player2_x].players)

    def test_playerX_playerY_should_be_correct_after_collision(self):
        self.player1.direction = Direction.left
        self.player1.speed = 2
        self.player1.x = 1
        self.player1.y = 0
        self.game.cells[self.player1.y][self.player1.x] = Cell([self.player1])

        with self.assertRaises(PlayerOutsidePlaygroundException):
            self.sut.get_and_visit_cells(self.player1, Action.speed_up)
        self.assertEqual(self.player1.x, 0)
        self.assertEqual(self.player1.y, 0)

    def test_playerX_playerY_should_be_correct_without_collision(self):
        self.player1.direction = Direction.left
        self.player1.speed = 2
        self.player1.x = 10
        self.player1.y = 0
        self.game.cells[self.player1.y][self.player1.x] = Cell([self.player1])

        self.sut.get_and_visit_cells(self.player1, Action.change_nothing)

        self.assertEqual(self.player1.x, 8)
        self.assertEqual(self.player1.y, 0)

    def test_correct_multiplier_should_be_returned_direction_up(self):
        self.player1.direction = Direction.up

        self.assertEqual((0, -1), self.sut.get_horizontal_and_vertical_multiplier(self.player1))

    def test_correct_multiplier_should_be_returned_direction_down(self):
        self.player1.direction = Direction.down

        self.assertEqual((0, 1), self.sut.get_horizontal_and_vertical_multiplier(self.player1))

    def test_correct_multiplier_should_be_returned_direction_left(self):
        self.player1.direction = Direction.left

        self.assertEqual((-1, 0), self.sut.get_horizontal_and_vertical_multiplier(self.player1))

    def test_correct_multiplier_should_be_returned_direction_right(self):
        self.player1.direction = Direction.right

        self.assertEqual((1, 0), self.sut.get_horizontal_and_vertical_multiplier(self.player1))
