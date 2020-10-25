from chillow.model.game import Game
from chillow.model.action import Action
from chillow.model.player import Player
from chillow.model.direction import Direction
from chillow.game_services.turn import Turn


class GameService():

    def __init__(self, game: Game):
        self.game = game
        self.turn = Turn(self.players, game.deadline)

    def do_action(self, player: Player, action: Action):
        pass

    def game_ended(self):
        pass
