from dataclasses import dataclass, field
from typing import List, Type, Any
from copy import deepcopy

from chillow.exceptions import MultipleActionByPlayerError, DeadLineExceededException, PlayerSpeedNotInRangeException, \
    PlayerOutsidePlaygroundException
from chillow.model.action import Action
from chillow.model.game import Game
from chillow.service.game_service import GameService


@dataclass
class SearchTreeRoot(object):
    __game: Game
    __children: List[Type['SearchTreeNode']] = field(default_factory=list, init=False)

    def __append_child(self, node):
        self.__children.append(node)

    def calculate_action(self, combinations: list[tuple[Any]], depth: int, turn_counter: int):
        if depth <= 0:
            raise Exception

        if depth == 1:
            for combination in combinations:
                node = SearchTreeRoot.__try_combination(self.__game, combination, turn_counter)
                self.__append_child(node)

            for child in self.__children:
                if child.is_win():
                    return child.get_action()
            return None

        for child in self.__children:
            action = child.create_combinations(deepcopy(combinations), depth - 1, turn_counter + 1)
            if action is not None:
                return self.select_action(action)

    @staticmethod
    def __try_combination(game: Game, combination: tuple[Action], turn_counter: int):
        modified_game = deepcopy(game)
        game_service = GameService(modified_game)
        game_service.turn.turn_ctr = turn_counter
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
        return SearchTreeNode(deepcopy(modified_game), deepcopy(own_action))

    def select_action(self, action: Action) -> Action:
        return action

    def is_win(self) -> bool:
        if not self.__game.you.active:
            return False

        for child in self.__children:
            if not child.is_win():
                return False

        return True

    # Todo: Anpassen
    def evaluate(self) -> int:
        if not self.__game.you.active:
            return 0

        evaluation = 1
        for child in self.__children:
            evaluation += child.evaluate()
        return evaluation


@dataclass
class SearchTreeNode(SearchTreeRoot):
    __action: Action

    def get_action(self):
        return self.__action

    def select_action(self, action: Action) -> Action:
        return self.__action
