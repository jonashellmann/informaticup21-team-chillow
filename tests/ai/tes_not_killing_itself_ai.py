import unittest
from datetime import datetime, timezone
from typing import List

from chillow.ai.not_killing_Itself_ai import NotKillingItselfAI
from chillow.model.action import Action
from chillow.model.cell import Cell
from chillow.model.direction import Direction
from chillow.model.game import Game
from chillow.model.player import Player
from chillow.service.game_service import GameService


class NotKillingItselfAITest(unittest.TestCase):

    def setUp(self):
        pass

    def test_ai_should_choose_the_own_non_killing_itself_action(self):
        self.player1 = Player(1, 0, 0, Direction.up, 1, True, "")
        self.player2 = Player(2, 4, 4, Direction.down, 3, True, "")
        self.players = [self.player1, self.player2]
        cells = [[Cell([self.player1]), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell([self.player2])]]

        time = datetime(2020, 10, 1, 12, 5, 13, 0, timezone.utc)
        game = Game(5, 5, cells, self.players, 2, True, time)
        game_service = GameService(game)
        sut = NotKillingItselfAI(self.player1, game, [], 3, 0)

        actions: List[Action] = sut.find_surviving_actions(game_service)

        self.assertTrue(Action.turn_right in actions)
        self.assertTrue(len(actions) == 1)

    def test_ai_should_choose_the_correct_list_of_actions_non_killing_itself(self):
        self.player1 = Player(1, 0, 1, Direction.up, 1, True, "")
        self.player2 = Player(2, 4, 4, Direction.down, 3, True, "")
        self.players = [self.player1, self.player2]
        cells = [[Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell([self.player1]), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell([self.player2])]]

        time = datetime(2020, 10, 1, 12, 5, 13, 0, timezone.utc)
        game = Game(5, 5, cells, self.players, 2, True, time)
        game_service = GameService(game)
        sut = NotKillingItselfAI(self.player1, game, [], 3, 0)

        actions: List[Action] = sut.find_surviving_actions(game_service)

        self.assertTrue(Action.change_nothing in actions)
        self.assertTrue(Action.turn_right in actions)
        self.assertTrue(len(actions) == 2)

    def test_ai_should_choose_the_correct_list_of_actions_non_killing_itself2(self):
        self.player1 = Player(1, 1, 2, Direction.up, 1, True, "")
        self.player2 = Player(2, 1, 1, Direction.down, 3, True, "")
        self.players = [self.player1, self.player2]
        cells = [[Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell([self.player2]), Cell(), Cell(), Cell()],
                 [Cell(), Cell([self.player1]), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell()]]

        time = datetime(2020, 10, 1, 12, 5, 13, 0, timezone.utc)
        game = Game(5, 5, cells, self.players, 2, True, time)
        game_service = GameService(game)
        sut = NotKillingItselfAI(self.player1, game, [], 3, 0)

        actions: List[Action] = sut.find_surviving_actions(game_service)

        self.assertTrue(Action.turn_left in actions)
        self.assertTrue(Action.turn_right in actions)
        self.assertTrue(len(actions) == 2)

    def test_ai_should_choose_the_correct_list_of_actions_non_killing_itself_in_turn_6(self):
        self.player1 = Player(1, 0, 4, Direction.up, 3, True, "")
        self.player2 = Player(2, 0, 1, Direction.down, 3, True, "")
        self.players = [self.player1, self.player2]
        cells = [[Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell([self.player2]), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell([self.player1]), Cell(), Cell(), Cell(), Cell()]]
        time = datetime(2020, 10, 1, 12, 5, 13, 0, timezone.utc)
        game = Game(5, 5, cells, self.players, 2, True, time)
        game_service = GameService(game)
        game_service.turn.turn_ctr = 6
        sut = NotKillingItselfAI(self.player1, game, [], 4, 0)

        actions: List[Action] = sut.find_surviving_actions(game_service)

        self.assertTrue(Action.slow_down in actions)
        self.assertTrue(Action.turn_right in actions)
        self.assertTrue(Action.speed_up in actions)
        self.assertTrue(len(actions) == 3)

    def test_ai_should_not_choose_speed_up_if_max_speed_is_allready_reached(self):
        MAX_SPEED = 3
        self.player1 = Player(1, 0, 4, Direction.up, MAX_SPEED, True, "")
        self.player2 = Player(2, 0, 1, Direction.down, 3, True, "")
        self.players = [self.player1, self.player2]
        cells = [[Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell([self.player2]), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell([self.player1]), Cell(), Cell(), Cell(), Cell()]]
        time = datetime(2020, 10, 1, 12, 5, 13, 0, timezone.utc)
        game = Game(5, 5, cells, self.players, 2, True, time)
        game_service = GameService(game)
        sut = NotKillingItselfAI(self.player1, game, [], MAX_SPEED, 0)

        actions: List[Action] = sut.find_surviving_actions(game_service)

        self.assertTrue(Action.slow_down in actions)
        self.assertTrue(Action.turn_right in actions)
        self.assertTrue(len(actions) == 2)

    def test_ai_should_calc_action_with_max_distance(self):
        self.player1 = Player(1, 0, 4, Direction.up, 1, True, "")
        self.player2 = Player(2, 0, 1, Direction.down, 3, True, "")
        self.players = [self.player1, self.player2]
        cells = [[Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell([self.player2]), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell([self.player1]), Cell(), Cell(), Cell(), Cell()]]
        time = datetime(2020, 10, 1, 12, 5, 13, 0, timezone.utc)
        game = Game(5, 5, cells, self.players, 2, True, time)
        game_service = GameService(game)
        sut = NotKillingItselfAI(self.player1, game, [], 3, 0)

        actions: List[Action] = sut.calc_action_with_max_distance_to_visited_cells(game_service, [Action.speed_up,
                                                                                                  Action.change_nothing,
                                                                                                  Action.turn_right])

        self.assertTrue(Action.turn_right in actions)
        self.assertTrue(len(actions) == 1)

    def test_ai_should_calc_all_action_with_max_distance_with_max_worse_distance(self):
        MAX_WORSE_DISTANCE = 1
        self.player1 = Player(1, 0, 4, Direction.up, 1, True, "")
        self.player2 = Player(2, 4, 4, Direction.down, 3, True, "")
        self.players = [self.player1, self.player2]
        cells = [[Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell(), Cell(), Cell(), Cell(), Cell()],
                 [Cell([self.player1]), Cell(), Cell(), Cell(), Cell([self.player2])]]
        time = datetime(2020, 10, 1, 12, 5, 13, 0, timezone.utc)
        game = Game(5, 5, cells, self.players, 2, True, time)
        game_service = GameService(game)
        sut = NotKillingItselfAI(self.player1, game, [], 3, MAX_WORSE_DISTANCE)

        actions: List[Action] = sut.calc_action_with_max_distance_to_visited_cells(game_service, [Action.speed_up,
                                                                                                  Action.change_nothing,
                                                                                                  Action.turn_right])

        self.assertTrue(Action.speed_up in actions)
        self.assertTrue(Action.change_nothing in actions)
        self.assertTrue(Action.turn_right in actions)
        self.assertTrue(len(actions) == 3)
