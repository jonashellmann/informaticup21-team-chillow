from chillow.controller import OfflineController
from chillow.view.headless_view import HeadlessView


class OfflineEvaluationController(OfflineController):

    def __init__(self, runs: int):
        super().__init__(HeadlessView())
        self.__participants = {}
        self.__results = {}
        self.__runs = runs

    def play(self):
        for _ in range(self.__runs):
            super().play()

            winner_player = self._game.get_winner()
            for ai in self._ais:
                ai_info = ai.get_information()

                # Save how often an AI configuration participated in a game
                if ai_info in self.__participants:
                    self.__participants[ai_info] += 1
                else:
                    self.__participants[ai_info] = 1

                # Save how often an AI configuration won a game
                if ai.player == winner_player:
                    if ai_info in self.__results:
                        self.__results[ai_info] += 1
                    else:
                        self.__results[ai_info] = 1

        print("----- Participants -----")
        print(self.__participants)
        print("------- Winners --------")
        print(self.__results)
