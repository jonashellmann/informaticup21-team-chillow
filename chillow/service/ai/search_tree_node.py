from dataclasses import dataclass
from typing import Type, Any, List, Tuple, Optional

from chillow.exceptions import InvalidPlayerMoveException
from chillow.model.action import Action
from chillow.model.game import Game
from chillow.model.player import Player
from chillow.service.game_service import GameService


@dataclass
class SearchTreeRoot(object):
    """TODO

    """

    _game: Game

    def calculate_action(self, player: Player, player_ids_to_watch: List[int], combinations: List[Tuple[Any]],
                         depth: int, turn_counter: int, root: bool, first_actions: List[Action], max_speed: int = 10,
                         randomize: bool = False) \
            -> Optional[Action]:
        """TODO

        Args:
            player:
            player_ids_to_watch:
            combinations:
            depth:
            turn_counter:
            root:
            first_actions:
            max_speed:
            randomize:

        Returns:

        """

        assert len(player_ids_to_watch) == len(combinations[0])

        if depth <= 0:
            raise Exception

        if depth == 1:
            for action in SearchTreeRoot.__get_actions(root, first_actions, randomize):
                child = self.__create_child(player, action, turn_counter, max_speed)
                if child is not None and child._game.get_player_by_id(player.id).active:
                    if SearchTreeRoot.__try_combinations_for_child(child, player, player_ids_to_watch, combinations,
                                                                   turn_counter):
                        return child.get_action()
            return None

        for action in SearchTreeRoot.__get_actions(root, first_actions, randomize):
            child = self.__create_child(player, action, turn_counter, max_speed)
            if child is not None and child._game.get_player_by_id(player.id).active:
                for combination in combinations:
                    node = SearchTreeRoot.__try_combination(child._game, player_ids_to_watch, combination, turn_counter)
                    if node._game.get_player_by_id(player.id).active:
                        node_action = node.calculate_action(player, player_ids_to_watch, combinations, depth - 1,
                                                            turn_counter + 1, False, first_actions, max_speed,
                                                            randomize)
                        if node_action is not None:
                            return child.get_action()

    @staticmethod
    def __get_actions(root: bool, first_actions: List[Action], randomize: bool) -> List[Action]:
        """TODO

        Args:
            root:
            first_actions:
            randomize:

        Returns:

        """

        if root and first_actions is not None and len(first_actions) >= 1:
            return first_actions
        return Action.get_actions(randomize)

    def __create_child(self, player: Player, action: Action, turn_counter: int, max_speed: int):
        """TODO

        Args:
            player:
            action:
            turn_counter:
            max_speed:

        Returns:

        """

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
                                     player_ids_to_watch: List[int],
                                     combinations: List[Tuple[Action]],
                                     turn_counter: int) -> bool:
        """ TODO

        Args:
            child:
            player:
            player_ids_to_watch:
            combinations:
            turn_counter:

        Returns:

        """

        for combination in combinations:
            node = SearchTreeRoot.__try_combination(child._game, player_ids_to_watch, combination, turn_counter)
            if not node._game.get_player_by_id(player.id).active:
                return False
        return True

    @staticmethod
    def __try_combination(game: Game, player_ids_to_watch: List[int], combination: Tuple[Action],
                          turn_counter: int):
        """TODO

        Args:
            game:
            player_ids_to_watch:
            combination:
            turn_counter:

        Returns:

        """

        modified_game = game.copy()
        game_service = GameService(modified_game)
        game_service.turn.turn_ctr = turn_counter
        players = modified_game.get_players_by_ids(player_ids_to_watch)
        for j in range(len(combination)):
            action = combination[j]
            player = players[j]
            SearchTreeRoot.__perform_simulation(game_service, action, player)

        game_service.check_and_set_died_players()
        return SearchTreeRoot(modified_game.copy())

    @staticmethod
    def __perform_simulation(game_service: GameService, action: Action, player: Player):
        """ TODO

        Args:
            game_service:
            action:
            player:

        Returns:

        """

        if player.active:
            try:
                game_service.visited_cells_by_player[player.id] = \
                    game_service.get_and_visit_cells(player, action)
            except InvalidPlayerMoveException:
                game_service.set_player_inactive(player)

    def get_action(self):
        return None


@dataclass
class SearchTreeNode(SearchTreeRoot):
    """TODO

    """

    __action: Action

    def get_action(self):
        return self.__action
