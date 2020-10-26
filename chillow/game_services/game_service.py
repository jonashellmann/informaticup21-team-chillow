from chillow.game_services.exceptions import MultipleActionByPlayerError, DeadLineExceededException
from chillow.model.game import Game
from chillow.model.action import Action
from chillow.model.player import Player
from chillow.model.direction import Direction
from chillow.game_services.turn import Turn


class GameService:

    def __init__(self, game: Game):
        self.game = game
        self.turn = Turn(self.game.players, game.deadline)

    def do_action(self, player: Player, action: Action):
        try:
            self.turn.action(player)
        except (MultipleActionByPlayerError, DeadLineExceededException) as exc:
            player.active = False

        self.game.running = self.is_game_ended()

    def is_game_ended(self) -> bool:
        active_player_ctr = 0
        for player in self.game.players:
            if player.active:
                active_player_ctr += 1
        return True if active_player_ctr < 2 else False
