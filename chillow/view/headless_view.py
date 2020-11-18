from chillow.model.game import Game
from chillow.view.view import View


class HeadlessView(View):

    def __init__(self):
        colors = ['red', 'blue', 'green', 'yellow', 'magenta', 'cyan']
        super().__init__(colors)

    def update(self, game: Game):
        pass

    def read_next_action(self):
        pass

    def end(self):
        pass
