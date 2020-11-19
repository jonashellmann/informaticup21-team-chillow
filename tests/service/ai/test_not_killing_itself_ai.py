import unittest
from datetime import datetime, timezone
from typing import List

from chillow.service.ai.not_killing_itself_ai import NotKillingItselfAI
from chillow.model.action import Action
from chillow.model.cell import Cell
from chillow.model.direction import Direction
from chillow.model.game import Game
from chillow.model.player import Player
from chillow.service.game_service import GameService


class NotKillingItselfAITest(unittest.TestCase):

    def test_ai_should_choose_the_own_non_killing_itself_action(self):
        player1 = Player(1, 0, 0, Direction.up, 1, True, "")
        player2 = Player(2, 4, 4, Direction.down, 3, True, "")
        players = [player1, player2]
        cells = [[Cell([player1]), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell([player2])]]

        time = datetime(2020, 10, 1, 12, 5, 13, 0, timezone.utc)
        game = Game(5, 5, cells, players, 2, True, time)
        game_service = GameService(game)
        sut = NotKillingItselfAI(player1, [], 3, 0)

        actions: List[Action] = sut.find_surviving_actions(game_service)

        self.assertTrue(Action.turn_right in actions)
        self.assertTrue(len(actions) == 1)

    def test_ai_should_choose_the_correct_list_of_actions_non_killing_itself(self):
        player1 = Player(1, 0, 1, Direction.up, 1, True, "")
        player2 = Player(2, 4, 4, Direction.down, 3, True, "")
        players = [player1, player2]
        cells = [[Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell([player1]), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell([player2])]]

        time = datetime(2020, 10, 1, 12, 5, 13, 0, timezone.utc)
        game = Game(5, 5, cells, players, 2, True, time)
        game_service = GameService(game)
        sut = NotKillingItselfAI(player1, [], 3, 0)

        actions: List[Action] = sut.find_surviving_actions(game_service)

        self.assertTrue(Action.change_nothing in actions)
        self.assertTrue(Action.turn_right in actions)
        self.assertTrue(len(actions) == 2)

    def test_ai_should_choose_the_correct_list_of_actions_non_killing_itself2(self):
        player1 = Player(1, 1, 2, Direction.up, 1, True, "")
        player2 = Player(2, 1, 1, Direction.down, 3, True, "")
        players = [player1, player2]
        cells = [[Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell([player2]), Cell(), Cell(), Cell()],
                 [Cell(), Cell([player1]), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell()]]

        time = datetime(2020, 10, 1, 12, 5, 13, 0, timezone.utc)
        game = Game(5, 5, cells, players, 2, True, time)
        game_service = GameService(game)
        sut = NotKillingItselfAI(player1, [], 3, 0)

        actions: List[Action] = sut.find_surviving_actions(game_service)

        self.assertTrue(Action.turn_left in actions)
        self.assertTrue(Action.turn_right in actions)
        self.assertTrue(len(actions) == 2)

    def test_ai_should_choose_the_correct_list_of_actions_non_killing_itself_in_turn_6(self):
        player1 = Player(1, 0, 4, Direction.up, 3, True, "")
        player2 = Player(2, 0, 1, Direction.down, 3, True, "")
        players = [player1, player2]
        cells = [[Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell([player2]), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell([player1]), Cell(), Cell(), Cell(), Cell()]]
        time = datetime(2020, 10, 1, 12, 5, 13, 0, timezone.utc)
        game = Game(5, 5, cells, players, 2, True, time)
        game_service = GameService(game)
        game_service.turn.turn_ctr = 6
        sut = NotKillingItselfAI(player1, [], 4, 0)

        actions: List[Action] = sut.find_surviving_actions(game_service)

        self.assertTrue(Action.slow_down in actions)
        self.assertTrue(Action.turn_right in actions)
        self.assertTrue(Action.speed_up in actions)
        self.assertTrue(len(actions) == 3)

    def test_ai_should_not_choose_speed_up_if_max_speed_is_allready_reached(self):
        MAX_SPEED = 3
        player1 = Player(1, 0, 4, Direction.up, MAX_SPEED, True, "")
        player2 = Player(2, 0, 1, Direction.down, 3, True, "")
        players = [player1, player2]
        cells = [[Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell([player2]), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell([player1]), Cell(), Cell(), Cell(), Cell()]]
        time = datetime(2020, 10, 1, 12, 5, 13, 0, timezone.utc)
        game = Game(5, 5, cells, players, 2, True, time)
        game_service = GameService(game)
        sut = NotKillingItselfAI(player1, [], MAX_SPEED, 0)

        actions: List[Action] = sut.find_surviving_actions(game_service)

        self.assertTrue(Action.slow_down in actions)
        self.assertTrue(Action.turn_right in actions)
        self.assertTrue(len(actions) == 2)

    def test_ai_should_calc_action_with_max_distance(self):
        player1 = Player(1, 0, 4, Direction.up, 1, True, "")
        player2 = Player(2, 0, 1, Direction.down, 3, True, "")
        players = [player1, player2]
        cells = [[Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell([player2]), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell([player1]), Cell(), Cell(), Cell(), Cell()]]
        time = datetime(2020, 10, 1, 12, 5, 13, 0, timezone.utc)
        game = Game(5, 5, cells, players, 2, True, time)
        game_service = GameService(game)
        sut = NotKillingItselfAI(player1, [], 3, 0)

        actions: List[Action] = sut.calc_action_with_max_distance_to_visited_cells(game_service, [Action.speed_up,
                                                                                                  Action.change_nothing,
                                                                                                  Action.turn_right])

        self.assertTrue(Action.turn_right in actions)
        self.assertTrue(len(actions) == 1)

    def test_ai_should_calc_all_action_with_max_distance_with_max_worse_distance(self):
        MAX_WORSE_DISTANCE = 1
        player1 = Player(1, 0, 4, Direction.up, 1, True, "")
        player2 = Player(2, 4, 4, Direction.down, 3, True, "")
        players = [player1, player2]
        cells = [[Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell([player1]), Cell(), Cell(), Cell(), Cell([player2])]]
        time = datetime(2020, 10, 1, 12, 5, 13, 0, timezone.utc)
        game = Game(5, 5, cells, players, 2, True, time)
        game_service = GameService(game)
        sut = NotKillingItselfAI(player1, [], 3, MAX_WORSE_DISTANCE)

        actions: List[Action] = sut.calc_action_with_max_distance_to_visited_cells(game_service, [Action.speed_up,
                                                                                                  Action.change_nothing,
                                                                                                  Action.turn_right])

        self.assertTrue(Action.speed_up in actions)
        self.assertTrue(Action.change_nothing in actions)
        self.assertTrue(Action.turn_right in actions)
        self.assertTrue(len(actions) == 3)

    def test_get_information(self):
        player = Player(1, 0, 4, Direction.up, 1, True, "")
        sut = NotKillingItselfAI(player, [], 3, 1)
        expected = "max_speed=3, max_worse_distance=1"

        result = sut.get_information()

        self.assertEqual(expected, result)
