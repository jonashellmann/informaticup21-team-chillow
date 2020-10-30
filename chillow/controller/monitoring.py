import os
import random
import sys
import time

from chillow.model.action import Action

if not os.getenv("DEACTIVATE_PYGAME", False):
    import pygame

from tabulate import tabulate
from abc import ABCMeta, abstractmethod

from chillow.model.game import Game


class Monitoring(metaclass=ABCMeta):

    @abstractmethod
    def update(self, game: Game):
        raise NotImplementedError

    @abstractmethod
    def create_next_action(self):
        raise NotImplementedError

    @abstractmethod
    def end(self):
        raise NotImplementedError


class ConsoleMonitoring(Monitoring):

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


class GraphicalMonitoring(Monitoring):
    RECTANGLE_SIZE = 10
    CLOCK_TICK = 60

    def __init__(self):
        self.clock = pygame.time.Clock()
        pygame.init()
        self.clock.tick(self.CLOCK_TICK)
        self.next_Action = True

        self.interface_initialized = False
        self.playerColors = {0: (0, 0, 0)}  # black if no Player is on the cell
        self.screen = None

    def update(self, game: Game):
        if not self.interface_initialized:
            self.initialize_interface(game)

        if not game.running:
            player = game.get_winner()
            print("Winner: Player " + str(player.id) + " (" + player.name + "). Your player ID was " + str(game.you.id))

        self.screen.fill((0, 0, 0))
        for row in range(game.height):
            for col in range(game.width):
                pygame.draw.rect(self.screen, self.playerColors[game.cells[row][col].get_player_id()],
                                 (col * self.RECTANGLE_SIZE + col,
                                  row * self.RECTANGLE_SIZE + row,
                                  self.RECTANGLE_SIZE,
                                  self.RECTANGLE_SIZE))
        pygame.display.update()
        self.clock.tick(60)

    def create_next_action(self) -> Action:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end()
                elif event.type == pygame.KEYDOWN:
                    pressed_key = pygame.key.get_pressed()
                    self.next_Action = False
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
                    self.next_Action = True

    def end(self):
        time.sleep(10)
        pygame.display.quit()
        pygame.quit()
        sys.exit()

    def initialize_interface(self, game: Game):
        self.interface_initialized = True
        colors = [(255, 61, 0), (156, 204, 101), (171, 71, 188), (38, 166, 154), (255, 238, 88), (66, 165, 245)]
        for i in range(0, len(game.players)):
            self.playerColors[int(game.players[i].id)] = colors[i]
        self.screen = pygame.display.set_mode(
            [game.width * self.RECTANGLE_SIZE + game.width, game.height * self.RECTANGLE_SIZE + game.height])
