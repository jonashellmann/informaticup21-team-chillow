from dataclasses import dataclass
from typing import Type, Any, List, Tuple

from chillow.exceptions import MultipleActionByPlayerError, DeadLineExceededException, PlayerSpeedNotInRangeException, \
    PlayerOutsidePlaygroundException
from chillow.model.action import Action
from chillow.model.game import Game
from chillow.model.player import Player
from chillow.service.game_service import GameService


@dataclass
class SearchTreeRoot(object):
    _game: Game

    def calculate_action(self, player: Player, combinations: List[Tuple[Any]], depth: int, turn_counter: int,
                         max_speed: int = 10, randomize: bool = False):
        if depth <= 0:
            raise Exception

        if depth == 1:
            for action in Action.get_actions(randomize):
                child = self.__create_child(player, action, turn_counter, max_speed)
                if child is not None and child._game.get_player_by_id(player.id).active:
                    if SearchTreeRoot.__try_combinations_for_child(child, player, combinations, turn_counter):
                        return child.get_action()
            return None

        for action in Action.get_actions(randomize):
            child = self.__create_child(player, action, turn_counter, max_speed)
            if child is not None and child._game.get_player_by_id(player.id).active:
                for combination in combinations:
                    node = SearchTreeRoot.__try_combination(child._game, player, combination, turn_counter)
                    if node._game.get_player_by_id(player.id).active:
                        node_action = node.calculate_action(player, combinations, depth - 1, turn_counter + 1)
                        if node_action is not None:
                            return child.get_action()

    def __create_child(self, player: Player, action: Action, turn_counter: int, max_speed: int):
        if player.speed == max_speed and action == Action.speed_up:
            return

        modified_game = self._game.copy()
        game_service = GameService(modified_game)
        game_service.turn.turn_ctr = turn_counter
        SearchTreeRoot.__perform_simulation(game_service, action, modified_game.get_player_by_id(player.id))
        game_service.check_and_set_died_players()

        return SearchTreeNode(modified_game.copy(), action)

    @staticmethod
    def __try_combinations_for_child(child: Type['SearchTreeRoot'],
                                     player: Player,
                                     combinations: List[Tuple[Action]],
                                     turn_counter: int) -> bool:
        for combination in combinations:
            node = SearchTreeRoot.__try_combination(child._game, player, combination, turn_counter)
            if not node._game.get_player_by_id(player.id).active:
                return False
        return True

    @staticmethod
    def __try_combination(game: Game, p: Player, combination: Tuple[Action], turn_counter: int):
        modified_game = game.copy()
        game_service = GameService(modified_game)
        game_service.turn.turn_ctr = turn_counter
        for j in range(len(combination)):
            action = combination[j]
            player = modified_game.get_other_players(p)[j]
            SearchTreeRoot.__perform_simulation(game_service, action, player)

        game_service.check_and_set_died_players()
        return SearchTreeRoot(modified_game.copy())

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


@dataclass
class SearchTreeNode(SearchTreeRoot):
    __action: Action

    def get_action(self) -> Action:
        return self.__action
