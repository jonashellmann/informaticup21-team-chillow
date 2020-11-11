from tabulate import tabulate

from chillow.model.action import Action
from chillow.model.game import Game
from chillow.view.view import View


class ConsoleView(View):

    def __init__(self):
        self.round = 0

    def update(self, game: Game):
        print("Round : ", self.round)
        self.round += 1

        table_player_ids = \
            [[' ' if cell.get_player_id() == 0 else cell.get_player_id() for cell in cells] for cells in game.cells]
        print(tabulate(table_player_ids, tablefmt="presto"))

        if not game.running:
            player = game.get_winner()
            print("Winner: Player " + str(player.id) + " (" + player.name + "). Your player ID was " + str(game.you.id))

    def create_next_action(self) -> Action:
        user_input = input("Input Next Action (l:turn_left, r:turn_right, u:speed_up, d:slow_down, "
                           "n:change_nothing): ")
        if user_input == "u":
            return Action.speed_up
        elif user_input == "d":
            return Action.slow_down
        elif user_input == "r":
            return Action.turn_right
        elif user_input == "l":
            return Action.turn_left
        elif user_input == "n":
            return Action.change_nothing

    def end(self):
        print("Game ended!")
