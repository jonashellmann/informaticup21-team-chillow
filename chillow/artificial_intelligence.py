import copy
import random

from abc import ABCMeta, abstractmethod
from typing import List
from enum import Enum

from chillow.game_services.game_service import GameService
from chillow.model.action import Action
from chillow.model.direction import Direction
from chillow.model.game import Game
from chillow.model.player import Player


class ArtificialIntelligence(metaclass=ABCMeta):

    def __init__(self, player: Player):
        self.player = player

    @abstractmethod
    def create_next_action(self, game: Game) -> Action:
        raise NotImplementedError


class ChillowAI(ArtificialIntelligence):

    def create_next_action(self, game: Game) -> Action:
        # Todo: Implement
        return random.choice(list(Action))


class AIOptions(Enum):
    max_distance, avoid_small_ares = range(2)


class NotKillingItselfAI(ArtificialIntelligence):

    def __init__(self, player: Player, game: Game, options: List[AIOptions]):
        self.player = player
        self.game = game
        self.turn_ctr = 0
        self.options = options

    def create_next_action(self, game: Game) -> Action:

        self.turn_ctr += 1

        game_service = GameService(game)
        game_service.turn.turn_ctr = self.turn_ctr

        surviving_actions = self.find_surviving_actions(game_service)
        if AIOptions.max_distance in self.options:
            max_distance_action = self.calc_action_with_max_distance_to_visited_cells(game_service, surviving_actions)
            return max_distance_action if max_distance_action is not None else Action.change_nothing
        else:
            return random.choice(surviving_actions) if surviving_actions is not None and len(
                surviving_actions) > 0 else Action.change_nothing

    def find_surviving_actions(self, game_service: GameService) -> [Action]:
        result: List[Action] = []
        for action in Action:  # select a surviving action
            gs_copy = copy.deepcopy(game_service)
            for player in gs_copy.game.players:
                if player.id == self.player.id:
                    try:
                        gs_copy.visited_cells_by_player[player.id] = gs_copy.get_and_visit_cells(player, action)
                    except Exception:
                        continue
                    gs_copy.check_and_set_died_players()
                    if player.active:
                        result += [action]

        return result

    def calc_action_with_max_distance_to_visited_cells(self, game_service: GameService,
                                                       actions: List[Action]) -> Action:
        max_straight_distance = 0
        best_action: Action = None
        for action in actions:
            gs_copy = copy.deepcopy(game_service)
            for player in gs_copy.game.players:
                if player.id == self.player.id:
                    try:
                        gs_copy.visited_cells_by_player[player.id] = gs_copy.get_and_visit_cells(player, action)

                        straight_distance = 0
                        vertical_multiplier = 0
                        horizontal_multiplier = 0
                        if player.direction == Direction.up:
                            vertical_multiplier = -1
                        elif player.direction == Direction.down:
                            vertical_multiplier = 1
                        elif player.direction == Direction.left:
                            horizontal_multiplier = -1
                        elif player.direction == Direction.right:
                            horizontal_multiplier = 1

                        for i in range(max(gs_copy.game.height, gs_copy.game.width)):
                            x = player.x + (i + 1) * horizontal_multiplier
                            y = player.y + (i + 1) * vertical_multiplier
                            if x in range(gs_copy.game.width) and y in range(gs_copy.game.height) and (
                                    gs_copy.game.cells[y][x].players is None or len(
                                gs_copy.game.cells[y][x].players) == 0):
                                straight_distance += 1
                            else:
                                break

                        if best_action is None or straight_distance > max_straight_distance:
                            max_straight_distance = straight_distance
                            best_action = action

                    except Exception:
                        continue

        return best_action
