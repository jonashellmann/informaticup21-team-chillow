import unittest
from datetime import datetime, timezone

import tests
from chillow.model.cell import Cell
from chillow.model.direction import Direction
from chillow.model.game import Game
from chillow.model.player import Player
from chillow.exceptions import WrongGameWidthException, WrongGameHeightException, OwnPlayerMissingException, \
    PlayerPositionException, PlayerWithGivenIdNotAvailableException
from chillow.service.data_loader import JSONDataLoader


class GameTest(unittest.TestCase):

    def test_examines_your_player_after_creation(self):
        player1 = Player(1, 0, 1, Direction.up, 0, True, "Name 1")
        player2 = Player(2, 1, 0, Direction.up, 0, True, "Name 2")
        player3 = Player(3, 0, 0, Direction.up, 0, True, "Name 3")
        players = [player1, player2, player3]
        cells = [[Cell([player3]), Cell([player2])], [Cell([player1]), Cell()]]

        game = Game(2, 2, cells, players, 2, True, datetime.now())

        self.assertEqual(game.you, player2)

    def test_raise_exception_on_non_existing_own_player(self):
        player1 = Player(1, 0, 1, Direction.up, 0, True, "Name 1")
        player3 = Player(3, 0, 0, Direction.up, 0, True, "Name 3")
        players = [player1, player3]
        cells = [[Cell([player3]), Cell([])], [Cell([player1]), Cell()]]

        with self.assertRaises(OwnPlayerMissingException):
            Game(2, 2, cells, players, 2, True, datetime.now())

    def test_raise_exception_on_wrong_player_position(self):
        player1 = Player(1, 1, 1, Direction.up, 0, True, "Name 1")
        player2 = Player(2, 0, 0, Direction.up, 0, True, "Name 2")
        player3 = Player(3, 0, 1, Direction.up, 0, True, "Name 3")
        players = [player1, player2, player3]
        cells = [[Cell([player2]), Cell([player3])], [Cell(), Cell([player1])]]

        with self.assertRaises(PlayerPositionException):
            Game(2, 2, cells, players, 2, True, datetime.now())

    def test_dont_raise_exception_on_wrong_inactive_player_position(self):
        player1 = Player(1, 1, 1, Direction.up, 0, False, "Name 1")
        player2 = Player(2, 1, 0, Direction.up, 0, True, "Name 2")
        player3 = Player(3, 0, 1, Direction.up, 0, True, "Name 3")
        players = [player1, player2, player3]
        cells = [[Cell([]), Cell([player2])], [Cell([player3]), Cell([player3])]]

        game = Game(2, 2, cells, players, 2, True, datetime.now())

        self.assertEqual(game.you, player2)

    def test_raise_exception_on_wrong_width(self):
        cells = [
            [
                Cell()
            ],
            [
                Cell(), Cell()
            ]
        ]

        with self.assertRaises(WrongGameWidthException):
            Game(2, 2, cells, [], 0, True, datetime.now())

    def test_raise_exception_on_wrong_height(self):
        cells = [
            [
                Cell(), Cell()
            ]
        ]

        with self.assertRaises(WrongGameHeightException):
            Game(2, 2, cells, [], 0, True, datetime.now())

    def test_find_winner_in_ended_game(self):
        player1 = Player(1, 0, 0, Direction.up, 0, False, "Name")
        player2 = Player(1, 1, 0, Direction.up, 0, True, "Name")
        cells = [[Cell([player1]), Cell([player2])]]
        game = Game(2, 1, cells, [player1, player2], 1, False, datetime.now())

        result = game.get_winner()

        self.assertEqual(game.get_winner(), result)

    def test_raise_exception_for_winner_in_running_game(self):
        player = Player(1, 0, 0, Direction.up, 0, True, "Name")
        cells = [[Cell([player]), Cell()]]
        game = Game(2, 1, cells, [player], 1, True, datetime.now())

        with self.assertRaises(Exception):
            game.get_winner()

    def test_raise_exception_for_no_winner_in_ended_game(self):
        player1 = Player(1, 0, 0, Direction.up, 0, True, "Name")
        player2 = Player(1, 1, 0, Direction.up, 0, True, "Name")
        cells = [[Cell([player1]), Cell([player2])]]
        game = Game(2, 1, cells, [player1, player2], 1, True, datetime.now())

        with self.assertRaises(Exception):
            game.get_winner()

    def test_player_with_id_should_be_returned(self):
        player1 = Player(1, 0, 0, Direction.up, 0, True, "Name")
        player2 = Player(2, 1, 0, Direction.up, 0, True, "Name")
        cells = [[Cell([player1]), Cell([player2])]]
        game = Game(2, 1, cells, [player1, player2], 1, True, datetime.now())

        self.assertEqual(player1, game.get_player_by_id(1))

    def test_raise_exception_when_player_id_invalid(self):
        player1 = Player(1, 1, 0, Direction.up, 0, True, "Name")
        player2 = Player(2, 0, 0, Direction.up, 0, True, "Name")
        cells = [[Cell([player2]), Cell([player1])]]
        game = Game(2, 1, cells, [player1, player2], 1, True, datetime.now())

        with self.assertRaises(PlayerWithGivenIdNotAvailableException):
            game.get_player_by_id(100)

    def test_return_all_players_except_one(self):
        player1 = Player(1, 1, 1, Direction.up, 0, True, "Name 1")
        player2 = Player(2, 1, 0, Direction.up, 0, True, "Name 2")
        player3 = Player(3, 0, 0, Direction.up, 0, True, "Name 3")
        players = [player1, player2, player3]
        cells = [[Cell([player3]), Cell([player2])], [Cell([]), Cell([player1])]]
        game = Game(2, 2, cells, players, 2, True, datetime.now())

        result = game.get_other_player_ids(player2)

        self.assertEqual([1, 3], result)

    def test_return_all_players_except_one_within_distance_1(self):
        player1 = Player(1, 3, 3, Direction.up, 0, True, "Name 1")
        player2 = Player(2, 1, 3, Direction.up, 0, True, "Name 2")
        player3 = Player(3, 0, 0, Direction.up, 0, True, "Name 3")
        players = [player1, player2, player3]
        cells = [
            [Cell([player3]), Cell(), Cell(), Cell(), Cell()],
            [Cell(), Cell(), Cell(), Cell(), Cell()],
            [Cell(), Cell(), Cell(), Cell(), Cell()],
            [Cell(), Cell([player2]), Cell(), Cell([player1]), Cell()],
            [Cell(), Cell(), Cell(), Cell(), Cell()]
        ]
        game = Game(5, 5, cells, players, 1, True, datetime.now())

        result = game.get_other_player_ids(player1, 2)

        self.assertEqual([2], result)

    def test_return_all_players_except_one_within_distance_2(self):
        player1 = Player(1, 4, 4, Direction.up, 0, True, "Name 1")
        player2 = Player(2, 2, 3, Direction.up, 0, True, "Name 2")
        player3 = Player(3, 1, 4, Direction.up, 0, True, "Name 3")
        players = [player1, player2, player3]
        cells = [
            [Cell(), Cell(), Cell(), Cell(), Cell()],
            [Cell(), Cell(), Cell(), Cell(), Cell()],
            [Cell(), Cell(), Cell(), Cell(), Cell()],
            [Cell(), Cell(), Cell([player2]), Cell(), Cell()],
            [Cell(), Cell([player3]), Cell([player2]), Cell(), Cell([player1])]
        ]
        game = Game(5, 5, cells, players, 1, True, datetime.now())

        result = game.get_other_player_ids(player1, 3)

        self.assertEqual([2], result)

    def test_translate_cell_matrix_to_pathfinding_matrix_should_be_correct(self):
        player1 = Player(1, 0, 0, Direction.up, 1, True, "")
        player2 = Player(2, 0, 1, Direction.down, 3, True, "")
        players = [player1, player2]
        cells = [[Cell([player1]), Cell()],
                 [Cell([player2]), Cell()],
                 [Cell(), Cell()]]

        game = Game(2, 3, cells, players, 2, True, datetime.now())
        expected_matrix = [[0, 1],
                           [0, 1],
                           [1, 1]]

        matrix = game.translate_cell_matrix_to_pathfinding_matrix()

        self.assertEqual(matrix, expected_matrix)

    def test_copying_a_game_should_return_same_game_but_different_identity(self):
        player1 = Player(1, 1, 1, Direction.up, 0, True, "Name")
        player2 = Player(2, 1, 0, Direction.up, 0, True, "Name2")
        player3 = Player(3, 0, 0, Direction.up, 0, True, "Name3")
        players = [player1, player2, player3]
        cells = [[Cell([player3]), Cell([player2])], [Cell([]), Cell([player1])]]
        game = Game(2, 2, cells, players, 2, True, datetime.now())

        result = game.copy()

        self.assertEqual(game, result)
        self.assertNotEqual(id(game), id(result))

    def test_normalize_game_deadline(self):
        server_time = datetime(2020, 11, 4, 14, 34, 43, 0, timezone.utc)
        own_time = datetime(2020, 11, 4, 14, 34, 40, 0, timezone.utc)
        game = JSONDataLoader().load(tests.read_test_file("ai/game_1.json"))
        expected = datetime(2020, 10, 1, 12, 5, 7, 0, timezone.utc)

        game.normalize_deadline(server_time, own_time)

        self.assertEqual(expected, game.deadline)
