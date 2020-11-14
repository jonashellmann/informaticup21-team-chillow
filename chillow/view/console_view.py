from tabulate import tabulate
from termcolor import colored

from chillow.model.action import Action
from chillow.model.game import Game
from chillow.view.view import View


class ConsoleView(View):

    def __init__(self):
        colors = ['red', 'blue', 'green', 'yellow', 'magenta', 'cyan']
        super().__init__(colors)
        self.__round = 0

    def update(self, game: Game):
        if not self._interface_initialized:
            self._initialize_interface(game)

        print("Round : ", self.__round)
        self.__round += 1

        table_player_ids = []
        for row in range(len(game.cells)):
            row_cells = []
            for col in range(len(game.cells[0])):
                cell = game.cells[row][col]
                if cell.get_player_id() == 0:
                    row_cells.append(' ')
                else:
                    player = game.get_player_by_id(cell.get_player_id())
                    color = self._player_colors[cell.get_player_id()]
                    if player.x == col and player.y == row:
                        if player == game.you:
                            row_cells.append(colored("x", color))
                        else:
                            row_cells.append(colored("o", color))
                    else:
                        row_cells.append(colored(str(player.id), color))
            table_player_ids.append(row_cells)

        print(tabulate(table_player_ids, tablefmt="jira")
              .replace(" ", "")
              .replace("||", "| |")
              .replace("||", "| |"))

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
