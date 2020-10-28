from itertools import product
from dataclasses import dataclass, field
from typing import List, Type
from copy import deepcopy

from chillow.ai.artificial_intelligence import ArtificialIntelligence
from chillow.exceptions import MultipleActionByPlayerError, DeadLineExceededException, PlayerSpeedNotInRangeException, \
    PlayerOutsidePlaygroundException
from chillow.model.action import Action
from chillow.model.game import Game
from chillow.model.player import Player
from chillow.service.game_service import GameService


class AlphaBetaPruningAI(ArtificialIntelligence):

    def __init__(self, player: Player, depth: int):
        super().__init__(player)
        self.__depth = depth

    @staticmethod
    def __get_combinations(player_count: int):
        return list(product(list(Action), repeat=player_count))

    def create_next_action(self, game: Game) -> Action:
        root = AlphaBetaNode(deepcopy(game))

        # So oft wie in self.__depth festgelegt
        combinations = AlphaBetaPruningAI.__get_combinations(len(game.players))
        for combination in combinations:
            modified_game = deepcopy(game)
            game_service = GameService(modified_game)
            own_action = None
            for i in range(len(modified_game.players)):
                action = combination[i]
                player = modified_game.players[i]
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
            root.append_child(AlphaBetaNode(deepcopy(modified_game), deepcopy(own_action)))

        return root.get_winning_action()


@dataclass
class AlphaBetaNode(object):

    __game: Game
    __action: Action = None
    __children: List[Type['AlphaBetaNode']] = field(default_factory=list, init=False)

    def append_child(self, node):
        self.__children.append(node)

    def evaluate(self) -> int:
        if not self.__game.you.active:
            return 0

        evaluation = 1
        for child in self.__children:
            evaluation += child.evaluate()
        return evaluation

    # Todo: Anpassen für weitere Tiefen im Baum
    def get_winning_action(self) -> Action:
        for child in self.__children:
            if child.evaluate() > 0:
                print(child.__game)
                return child.__action
