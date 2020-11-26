from tabulate import tabulate
from termcolor import colored

from chillow.model.action import Action
from chillow.model.game import Game
from chillow.view.view import View


class ConsoleView(View):
    """Uses the console as an UI and every output goes there."""

    def __init__(self):
        """Creates a new console view."""
        colors = ['red', 'blue', 'green', 'yellow', 'magenta', 'cyan']
        super().__init__(colors)
        self.__round = 0
        self.__player_representation = {}

    def update(self, game: Game):
        """See base class."""
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
                        row_cells.append(colored(str(self.__player_representation[player.id]), color))
            table_player_ids.append(row_cells)

        print(tabulate(table_player_ids, tablefmt="jira")
              .replace(" ", "")
              .replace("||", "| |")
              .replace("||", "| |"))

        if not game.running:
            player = game.get_winner()
            if player is None:
                print("No winner in game.")
            else:
                print("Winner: Player " + str(self.__player_representation[player.id]) + " (" + player.name +
                      "). Your player ID was " + str(self.__player_representation[game.you.id]))

    def read_next_action(self) -> Action:
        """See base class."""
        user_input = self.\
            get_input("Input Next Action (l:turn_left, r:turn_right, u:speed_up, d:slow_down, n:change_nothing): ")
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
        else:
            print("Wrong input: Action change_nothing returned")
            return Action.change_nothing

    @staticmethod
    def get_input(text: str):
        return input(text)

    def end(self):
        """See base class."""
        print("Game ended!")

    def _initialize_interface(self, game: Game):
        super()._initialize_interface(game)
        player_counter = 0
        for player in game.players:
            player_counter += 1
            self.__player_representation[player.id] = player_counter
