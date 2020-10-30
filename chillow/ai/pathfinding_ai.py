from random import choice

from chillow.ai.artificial_intelligence import ArtificialIntelligence
from chillow.model.action import Action
from chillow.model.game import Game
from chillow.model.player import Player
from chillow.service.game_service import GameService


class Pahtfinding_AI(ArtificialIntelligence):

    def __init__(self, player: Player, game: Game, max_speed):
        super().__init__(player)
        self.__game = game
        self.turn_ctr = 0
        self.__max_speed = max_speed

    def create_next_action(self, game: Game) -> Action:
        self.turn_ctr += 1
        game_service = GameService(game)
        game_service.turn.turn_ctr = self.turn_ctr

        surviving_actions = self.find_surviving_actions(game_service)

        return choice(surviving_actions) if len(surviving_actions) > 0 else choice()