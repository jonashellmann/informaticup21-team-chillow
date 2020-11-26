from chillow.model.game import Game
from chillow.view.view import View


class HeadlessView(View):
    """This view may be used when there is no need for any feedback on how the game is progressing.

    There is no UI and no human player can interact with the game using this view.
    """

    def __init__(self):
        """Creates a new headless view."""
        colors = ['red', 'blue', 'green', 'yellow', 'magenta', 'cyan']
        super().__init__(colors)

    def update(self, game: Game):
        """See base class"""
        pass

    def read_next_action(self):
        """See base class"""
        pass

    def end(self):
        """See base class"""
        pass
