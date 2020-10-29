from dataclasses import dataclass, field
from typing import List, Type, Any
from copy import deepcopy

from chillow.exceptions import MultipleActionByPlayerError, DeadLineExceededException, PlayerSpeedNotInRangeException, \
    PlayerOutsidePlaygroundException
from chillow.model.action import Action
from chillow.model.game import Game
from chillow.model.player import Player
from chillow.service.game_service import GameService


@dataclass
class SearchTreeRoot(object):
    _game: Game
    __children: List[Type['SearchTreeNode']] = field(default_factory=list, init=False)

    def append_child(self, node):
        self.__children.append(node)

    def calculate_action(self, player: Player, combinations: list[tuple[Any]], depth: int, turn_counter: int):
        if depth <= 0:
            raise Exception

        if depth == 1:
            for action in list(Action):
                child = self.__create_child(player, action, turn_counter)
                if child._game.get_player_by_id(player.id).active:
                    self.append_child(child)

            for child in self.__children:
                if SearchTreeRoot.__try_combinations_for_child(child, player, combinations, turn_counter):
                    return child.get_action()
            return None

        for action in list(Action):
            child = self.__create_child(player, action, turn_counter)
            if child._game.get_player_by_id(player.id).active:
                for combination in combinations:
                    node = SearchTreeRoot.__try_combination(child._game, player, combination, turn_counter)
                    if node._game.get_player_by_id(player.id).active:
                        child.append_child(node)
                        node_action = node.calculate_action(player, combinations, depth - 1, turn_counter + 1)
                        if node_action is not None:
                            return action

    def __create_child(self, player: Player, action: Action, turn_counter: int):
        modified_game = deepcopy(self._game)
        game_service = GameService(modified_game)
        game_service.turn.turn_ctr = turn_counter
        SearchTreeRoot.__perform_simulation(game_service, action, modified_game.get_player_by_id(player.id))
        game_service.check_and_set_died_players()

        return SearchTreeNode(deepcopy(modified_game), action)

    @staticmethod
    def __try_combinations_for_child(child: Type['SearchTreeRoot'],
                                     player: Player,
                                     combinations: list[tuple[Action]],
                                     turn_counter: int) -> bool:
        for combination in combinations:
            node = SearchTreeRoot.__try_combination(child._game, player, combination, turn_counter)
            if not node._game.get_player_by_id(player.id).active:
                return False
            child.append_child(node)
        return True

    @staticmethod
    def __try_combination(game: Game, p: Player, combination: tuple[Action], turn_counter: int):
        modified_game = deepcopy(game)
        game_service = GameService(modified_game)
        game_service.turn.turn_ctr = turn_counter
        for j in range(len(combination)):
            action = combination[j]
            player = modified_game.get_other_players(p)[j]
            SearchTreeRoot.__perform_simulation(game_service, action, player)

        game_service.check_and_set_died_players()
        return SearchTreeRoot(deepcopy(modified_game))

    @staticmethod
    def __perform_simulation(game_service: GameService, action: Action, player: Player):
        if player.active:
            try:
                game_service.visited_cells_by_player[player.id] = \
                    game_service.get_and_visit_cells(player, action)
            except (MultipleActionByPlayerError, DeadLineExceededException, PlayerSpeedNotInRangeException,
                    PlayerOutsidePlaygroundException):
                game_service.set_player_inactive(player)

    def get_action(self) -> Action:
        return None

    def select_action(self, action: Action) -> Action:
        return action


@dataclass
class SearchTreeNode(SearchTreeRoot):
    __action: Action

    def get_action(self) -> Action:
        return self.__action

    def select_action(self, action: Action) -> Action:
        return self.__action
