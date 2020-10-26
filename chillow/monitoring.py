import os
import random as rnd
import sys

from chillow.model.action import Action

if "DEACTIVATE_PYGAME" not in os.environ or not os.environ["DEACTIVATE_PYGAME"]:
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


class ConsoleMonitoring(Monitoring):

    def __init__(self):
        self.round = 0

    def update(self, game: Game):
        print("Round : ", self.round)
        self.round += 1

        table_player_ids =\
            [[' ' if cell.get_player_id() == 0 else cell.get_player_id() for cell in cells] for cells in game.cells]
        print(tabulate(table_player_ids, tablefmt="presto"))

    def create_next_action(self) -> Action:
        input = input("Input Next Aktcion(l:turn_left, r:turn_right, u:speed_up, d:slow_down, n:change_nothing): ")
        if input == "u":
            return Action.speed_up
        elif input == "d":
            return Action.slow_down
        elif input == "r":
            return Action.turn_right
        elif input == "l":
            return Action.turn_left
        elif input == "n":
            return Action.change_nothing

class GraphicalMonitoring(Monitoring):
    def __init__(self, game: Game):
        self.rectangleSize = 10
        self.game = game
        self.playerColors = {0: (0, 0, 0)}  # black if no Player is on the cell
        for i in range(0, len(game.players)):
            self.playerColors[int(game.players[i].id)] = (rnd.randint(0, 255), rnd.randint(0, 255), rnd.randint(0, 255))
        self.screen = pygame.display.set_mode(
            [game.width * self.rectangleSize, game.height * self.rectangleSize])
        self.clock = pygame.time.Clock()
        pygame.init()
        self.clock.tick(60)
        self.next_Action = True

    def update(self, game: Game):
        self.screen.fill((0, 0, 0))
        for row in range(game.width):
            for col in range(game.height):
                pygame.draw.rect(self.screen, self.playerColors[game.cells[row][col].get_player_id()],
                                 (col * self.rectangleSize,
                                  row * self.rectangleSize,
                                  self.rectangleSize,
                                  self.rectangleSize))
        pygame.display.update()
        self.clock.tick(60)

    def create_next_action(self) -> Action:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()  # closes the application
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