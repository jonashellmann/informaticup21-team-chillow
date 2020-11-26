from abc import ABCMeta, abstractmethod
from typing import List, Any

from chillow.model.game import Game


class View(metaclass=ABCMeta):
    """Provides an UI to show the game progress."""

    def __init__(self, colors: List[Any]):
        """Creates a new view.

        Args:
            colors:
                A list of values that define colors in the specific view.
                This may be human readable strings or strings with hex values.
                The list may not be empty.

        Raises:
            AssertionError: The parameter list is empty.
        """
        self._interface_initialized = False
        self._player_colors = {0: (0, 0, 0)}

        assert colors is not None and len(colors) > 0, "No colors available for interface"
        self.__colors = colors

    @abstractmethod
    def update(self, game: Game):
        """Updates the view with the new game state.

        Args:
            game: The state of the game that should be shown in the view.
        """
        pass

    @abstractmethod
    def read_next_action(self):
        """Reads the next action to be performed by a human player."""
        pass

    @abstractmethod
    def end(self):
        """Performs actions to shut down the view."""
        pass

    def _initialize_interface(self, game: Game):
        self._interface_initialized = True
        for i in range(0, len(game.players)):
            self._player_colors[int(game.players[i].id)] = self.__colors[i % (len(self.__colors) - 1)]
