from itertools import product
from copy import deepcopy

from chillow.ai.alpha_beta_node import AlphaBetaRoot, AlphaBetaNode
from chillow.ai.artificial_intelligence import ArtificialIntelligence
from chillow.exceptions import MultipleActionByPlayerError, DeadLineExceededException, PlayerSpeedNotInRangeException, \
    PlayerOutsidePlaygroundException
from chillow.model.action import Action
from chillow.model.game import Game
from chillow.model.player import Player
from chillow.service.game_service import GameService


# Todo: AI umbennen
# Todo: Zaehler für Zug ergaenzen wegen Lücken
class AlphaBetaPruningAI(ArtificialIntelligence):

    def __init__(self, player: Player, depth: int):
        super().__init__(player)
        self.__depth = depth

    def create_next_action(self, game: Game) -> Action:
        root = AlphaBetaRoot(deepcopy(game))
        combinations = AlphaBetaPruningAI.__get_combinations(len(game.players))

        for depth in range(self.__depth):
            for node in root.get_children(depth):
                for combination in combinations:
                    created_node = AlphaBetaPruningAI.__try_combination(game, combination)
                    node.append_child(created_node)

        return root.get_winning_action()

    @staticmethod
    def __get_combinations(player_count: int) -> list[tuple[Action]]:
        return list(product(list(Action), repeat=player_count))

    # Todo: Implementierung dieser Methode
    @staticmethod
    def __try_combination(game: Game, combination: tuple[Action]) -> AlphaBetaNode:
        modified_game = deepcopy(game)
        game_service = GameService(modified_game)
        own_action = None
        for j in range(len(modified_game.players)):
            action = combination[j]
            player = modified_game.players[j]
            if player.id == game.you.id:
                own_action = action
            if player.active:
                try:
                    game_service.visited_cells_by_player[player.id] = \
                        game_service.get_and_visit_cells(player, action)
                except (MultipleActionByPlayerError, DeadLineExceededException, PlayerSpeedNotInRangeException,
                        PlayerOutsidePlaygroundException):
                    game_service.set_player_inactive(player)
        game_service.check_and_set_died_players()
        return AlphaBetaNode(deepcopy(modified_game), deepcopy(own_action))
