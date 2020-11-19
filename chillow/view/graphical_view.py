import sys
import time
import pygame

from chillow.model.action import Action
from chillow.model.game import Game
from chillow.view.view import View


class GraphicalView(View):
    RECTANGLE_SIZE = 10
    CLOCK_TICK = 60

    def __init__(self):
        colors = [(255, 61, 0), (156, 204, 101), (171, 71, 188), (38, 166, 154), (255, 238, 88), (66, 165, 245)]
        super().__init__(colors)

        self.__clock = pygame.time.Clock()
        pygame.init()
        self.__clock.tick(self.CLOCK_TICK)
        self.__next_action = True
        self.__screen = None

    def update(self, game: Game):
        if not self._interface_initialized:
            self._initialize_interface(game)

        if not game.running:
            player = game.get_winner()
            if player is None:
                print("No winner in game.")
            else:
                print("Winner: Player " + str(player.id) + " (" + player.name + "). Your player ID was " +
                      str(game.you.id))

        self.__screen.fill((0, 0, 0))
        for row in range(game.height):
            for col in range(game.width):
                pygame.draw.rect(self.__screen,
                                 self._player_colors[game.cells[row][col].get_player_id()],
                                 (col * self.RECTANGLE_SIZE + col,
                                  row * self.RECTANGLE_SIZE + row,
                                  self.RECTANGLE_SIZE,
                                  self.RECTANGLE_SIZE))
                if game.cells[row][col].get_player_id() != 0:
                    player = game.get_player_by_id(game.cells[row][col].get_player_id())
                    if player.x == col and player.y == row:  # print head
                        border_width = 2
                        if player == game.you:
                            border_width = 4
                        pygame.draw.rect(self.__screen,
                                         self._player_colors[0],
                                         (col * self.RECTANGLE_SIZE + col + border_width,
                                          row * self.RECTANGLE_SIZE + row + border_width,
                                          self.RECTANGLE_SIZE - (2 * border_width),
                                          self.RECTANGLE_SIZE - (2 * border_width)))
        pygame.display.update()
        self.__clock.tick(60)

    def read_next_action(self) -> Action:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end()
                elif event.type == pygame.KEYDOWN:
                    pressed_key = pygame.key.get_pressed()
                    self.__next_action = False
                    if pressed_key[pygame.K_UP]:
                        return Action.speed_up
                    elif pressed_key[pygame.K_DOWN]:
                        return Action.slow_down
                    elif pressed_key[pygame.K_RIGHT]:
                        return Action.turn_right
                    elif pressed_key[pygame.K_LEFT]:
                        return Action.turn_left
                    elif pressed_key[pygame.K_SPACE]:
                        return Action.change_nothing
                elif event.type == pygame.KEYUP:
                    self.__next_action = True

    def end(self):
        time.sleep(10)
        pygame.display.quit()
        pygame.quit()
        sys.exit()

    def _initialize_interface(self, game: Game):
        super()._initialize_interface(game)
        self.__screen = pygame.display.set_mode(
            [game.width * self.RECTANGLE_SIZE + game.width, game.height * self.RECTANGLE_SIZE + game.height])
