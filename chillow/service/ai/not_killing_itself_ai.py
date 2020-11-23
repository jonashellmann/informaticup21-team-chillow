import copy
import logging
import pickle
from enum import Enum
from random import choice
from typing import List, Dict
from multiprocessing import Value

from chillow.exceptions import InvalidPlayerMoveException
from chillow.service.ai.artificial_intelligence import ArtificialIntelligence
from chillow.model.action import Action
from chillow.model.game import Game
from chillow.model.player import Player
from chillow.service.game_service import GameService


class AIOptions(Enum):
    max_distance = range(1)


class NotKillingItselfAI(ArtificialIntelligence):

    def __init__(self, player: Player, options: List[AIOptions], max_speed: int, max_worse_distance: int,
                 depth: int = 3):
        super().__init__(player, max_speed)
        self.options = options
        self.max_worse_distance = max_worse_distance
        self.depth = depth

    def get_information(self) -> str:
        return super().get_information() \
               + ", max_worse_distance=" + str(self.max_worse_distance)

    def create_next_action(self, game: Game, return_value: Value):
        self.turn_ctr += 1

        game_service = GameService(game)
        game_service.turn.turn_ctr = self.turn_ctr

        surviving_actions = self.find_surviving_actions_with_best_depth(game_service, self.depth)
        if AIOptions.max_distance in self.options:
            max_distance_actions = self.calc_action_with_max_distance_to_visited_cells(game_service, surviving_actions)
            action = choice(max_distance_actions) if max_distance_actions is not None and len(
                max_distance_actions) > 0 else Action.change_nothing
        else:
            action = choice(surviving_actions) if surviving_actions is not None and len(
                surviving_actions) > 0 else Action.change_nothing

        return_value.value = action.get_index()

    def calc_action_with_max_distance_to_visited_cells(self, game_service: GameService,
                                                       actions: List[Action]) -> List[Action]:
        max_straight_distance = 0
        best_actions: Dict[Action, int] = {}
        for action in actions:
            gs_copy = copy.deepcopy(game_service)
            try:
                player = gs_copy.game.get_player_by_id(self.player.id)
                gs_copy.visited_cells_by_player[player.id] = gs_copy.get_and_visit_cells(player, action)

                straight_distance = 0
                horizontal_multiplier, vertical_multiplier = GameService.get_horizontal_and_vertical_multiplier(player)

                for i in range(max(gs_copy.game.height, gs_copy.game.width)):
                    x = player.x + (i + 1) * horizontal_multiplier
                    y = player.y + (i + 1) * vertical_multiplier
                    if x in range(gs_copy.game.width) and y in range(gs_copy.game.height) and (
                            gs_copy.game.cells[y][x].players is None or len(gs_copy.game.cells[y][x].players) == 0):
                        straight_distance += 1
                    else:
                        break

                if len(best_actions) == 0 or straight_distance > max_straight_distance:
                    max_straight_distance = straight_distance
                    best_actions[action] = straight_distance
                    updated_best_actions: Dict[Action, int] = {}
                    for (act, dist) in best_actions.items():  # new max_straight_distance. Remove worth options
                        if dist >= max_straight_distance - self.max_worse_distance:
                            updated_best_actions[act] = dist
                    best_actions = updated_best_actions
                elif straight_distance >= max_straight_distance - self.max_worse_distance:  # still good option
                    best_actions[action] = straight_distance
            except Exception as ex:
                logging.warning(ex)
                continue

        return list(best_actions.keys())

    def find_surviving_actions(self, game_service: GameService, depth: int = 1) -> List[Action]:
        assert depth > 0, "depth must be greater than 0"

        result: List[Action] = []
        for action in Action:  # select a surviving action
            gs_copy = pickle.loads(pickle.dumps(game_service))
            try:
                player = gs_copy.game.get_player_by_id(self.player.id)
                if player.speed == self.max_speed and action == Action.speed_up:
                    continue
                gs_copy.visited_cells_by_player[player.id] = gs_copy.get_and_visit_cells(player, action)
            except InvalidPlayerMoveException:
                continue
            gs_copy.check_and_set_died_players()
            if player.active:
                interim_result = []
                if depth > 1:
                    interim_result = self.find_surviving_actions(gs_copy, depth - 1)
                if len(interim_result) > 0 or depth == 1:
                    result += [action]

        return result

    def find_surviving_actions_with_best_depth(self, game_service: GameService, depth: int) -> List[Action]:
        assert depth > 0, "depth must be greater than 0"
        result: List[Action] = []
        for current_depth in reversed(range(1, depth + 1)):
            result = self.find_surviving_actions(game_service, current_depth)
            if len(result) > 0:
                break

        return result
