import sys
import time

from chillow.model.action import Action
from chillow.model.cell import Cell
from chillow.model.game import Game
from chillow.view.view import View


class GraphicalView(View):
    """Provides a graphical UI using PyGame."""

    RECT_SIZE = 10
    CLOCK_TICK = 60

    def __init__(self, pygame):
        """Creates a new graphical view.

        Args:
            pygame: The PyGame library.
        """
        colors = [(255, 61, 0), (156, 204, 101), (171, 71, 188), (38, 166, 154), (255, 238, 88), (66, 165, 245)]
        super().__init__(colors)

        self.__pygame = pygame
        self.__clock = self.__pygame.time.Clock()
        pygame.init()
        self.__clock.tick(self.CLOCK_TICK)
        self.__next_action = True  # Flag to wait for a KEYUP event.
        # Otherwise the user is doing multiple actions with one click.
        self.__screen = None

    def update(self, game: Game):
        """See base class."""
        if not self._interface_initialized:
            self._initialize_interface(game)

        if not game.running:
            player = game.get_winner()
            if player is None:
                print("No winner in game.")
            else:
                print("Winner: Player " + str(player.id) + " (" + player.name + "). Your player ID was " +
                      str(game.you.id) + ".")

        self.__screen.fill((0, 0, 0))  # black background
        for row in range(game.height):
            for col in range(game.width):
                self.__pygame.draw.rect(self.__screen,
                                        self.__get_player_color(game.cells[row][col]),
                                        (col * self.RECT_SIZE + col,
                                         row * self.RECT_SIZE + row,
                                         self.RECT_SIZE,
                                         self.RECT_SIZE))
                if game.cells[row][col].get_player_id() != 0:
                    player = game.get_player_by_id(game.cells[row][col].get_player_id())
                    if player.x == col and player.y == row:  # print head
                        border_width = 2
                        if player == game.you:
                            border_width = 4  # head of the own player has a smaller dot
                        self.__pygame.draw.rect(self.__screen,
                                                self._player_colors[0],
                                                (col * self.RECT_SIZE + col + border_width,
                                                 row * self.RECT_SIZE + row + border_width,
                                                 self.RECT_SIZE - (2 * border_width),
                                                 self.RECT_SIZE - (2 * border_width)))
        self.__pygame.display.update()
        self.__clock.tick(60)

    def __get_player_color(self, cell: Cell):
        return self._player_colors[cell.get_player_id()]

    def read_next_action(self) -> Action:  # noqa: C901
        """See base class."""
        while True:
            for event in self.__pygame.event.get():
                if event.type == self.__pygame.QUIT:  # Allows to close the pygame-window
                    self.end()
                    return Action.get_default()
                elif event.type == self.__pygame.KEYDOWN:
                    pressed_key = self.__pygame.key.get_pressed()
                    self.__next_action = False
                    if pressed_key[self.__pygame.K_UP]:
                        return Action.speed_up
                    elif pressed_key[self.__pygame.K_DOWN]:
                        return Action.slow_down
                    elif pressed_key[self.__pygame.K_RIGHT]:
                        return Action.turn_right
                    elif pressed_key[self.__pygame.K_LEFT]:
                        return Action.turn_left
                    elif pressed_key[self.__pygame.K_SPACE]:
                        return Action.change_nothing
                elif event.type == self.__pygame.KEYUP:
                    self.__next_action = True

    def end(self):
        """See base class."""
        time.sleep(10)
        self.__pygame.display.quit()
        self.__pygame.quit()
        sys.exit()

    def _initialize_interface(self, game: Game):
        super()._initialize_interface(game)
        self.__screen = self.__pygame.display.set_mode(
            [game.width * self.RECT_SIZE + game.width, game.height * self.RECT_SIZE + game.height])
