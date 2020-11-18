from chillow.controller import OfflineController
from chillow.view.headless_view import HeadlessView


class OfflineEvaluationController(OfflineController):

    def __init__(self, runs: int):
        super().__init__(HeadlessView())
        self.__results = {}
        self.__runs = runs

    def play(self):
        for i in range(self.__runs):
            print("Run: " + str(i))

            super().play()
            winner_player = self._game.get_winner()
            for ai in self._ais:
                if ai.player == winner_player:
                    winner_class = ai.__class__.__name__
                    if winner_class in self.__results:
                        self.__results[winner_class] += 1
                    else:
                        self.__results[winner_class] = 1

        print(self.__results)
