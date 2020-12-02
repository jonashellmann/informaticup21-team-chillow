from typing import List
from multiprocessing import Value

from chillow.service.ai.search_tree_node import SearchTreeRoot
from chillow.service.ai.artificial_intelligence import ArtificialIntelligence
from chillow.model.action import Action
from chillow.model.game import Game
from chillow.model.player import Player


class SearchTreeAI(ArtificialIntelligence):
    """The SearchTreeAI tries to create a tree by simulating different actions for all player for the next rounds.

    If there is an initial action that lets the player survive for the next rounds not depending on which action
    the other players will make, this action will be chosen.

    Attributes:
        player: The player associated with this AI.
    """

    def __init__(self, player: Player, depth: int, max_speed: int = 10, randomize: bool = False,
                 distance_to_check: int = 0):
        """ Creates a new object of the SearchTreeAI.

        Args:
            player: The player assigned to the AI.
            max_speed: The maximum speed the AI can reach.
            depth: Depth pre-calculating actions.
            randomize: Indicating whether to calculate actions in tree in random order.
            distance_to_check:
                Distance an enemy player is allowed to be at maximum distance, so that he is taken into
                account in the calculations.
        """

        super().__init__(player, max_speed)
        self.__depth = depth
        self.__randomize = randomize
        self.__distance_to_check = distance_to_check

    def get_information(self) -> str:
        """See base class."""
        return (super().get_information() +
                ", depth=" + str(self.__depth) +
                ", randomize=" + str(self.__randomize) +
                ", distance_to_check=" + str(self.__distance_to_check))

    def create_next_action(self, game: Game, return_value: Value):
        """See base class."""
        self._turn_ctr += 1

        root = SearchTreeRoot(game.copy())
        player_ids_to_watch = game.get_other_player_ids(self.player, self.__distance_to_check, True)
        combinations = Action.get_combinations(len(player_ids_to_watch))

        action = root.calculate_action(self.player, player_ids_to_watch, combinations, self.__depth, self._turn_ctr,
                                       True, [], self._max_speed, self.__randomize)
        return_value.value = (action if action is not None else Action.get_random_action()).get_index()

    def create_all_next_surviving_actions(self, game: Game) -> List[Action]:
        """Calculates not only one but all actions that will let the player survive for the next rounds.

        Args:
            game: The current state of the game.

        Returns:
            A list of actions which will let the player survive for the next rounds.
        """

        root = SearchTreeRoot(game.copy())
        player_ids_to_watch = game.get_other_player_ids(self.player, self.__distance_to_check, True)
        combinations = Action.get_combinations(len(player_ids_to_watch))

        search_tree_actions = []

        for action in Action.get_actions():
            if root.calculate_action(self.player, player_ids_to_watch, combinations, self.__depth, self._turn_ctr, True,
                                     [action], self._max_speed, True) is not None:
                search_tree_actions.append(action)

        return search_tree_actions

    def _get_depth(self) -> int:
        return self.__depth

    def _get_distance_to_check(self) -> int:
        return self.__distance_to_check
