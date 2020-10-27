import copy
import random

from abc import ABCMeta, abstractmethod
from typing import List

from chillow.game_services.game_service import GameService
from chillow.model.action import Action
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


class NotKillingItselfAI(ArtificialIntelligence):

    def __init__(self, player: Player, game: Game):
        self.player = player
        self.game = game
        self.turn_ctr = 0

    def create_next_action(self, game: Game) -> Action:
        result: List[Action] = []
        self.turn_ctr += 1

        game_service = GameService(game)
        game_service.turn.turn_ctr = self.turn_ctr

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

        return random.choice(result) if len(result) > 0 else Action.change_nothing
