import os
import random as rnd
if "DEACTIVATE_PYGAME" not in os.environ or not os.environ["DEACTIVATE_PYGAME"]:
    import pygame

from tabulate import tabulate
from abc import ABCMeta, abstractmethod

from chillow.model.game import Game


class Monitoring(metaclass=ABCMeta):

    @abstractmethod
    def update(self, game: Game):
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

    def update(self, game: Game):
        self.screen.fill((0, 0, 0))
        for row in range(game.width):
            for col in range(game.height):
                pygame.draw.rect(self.screen, self.playerColors[game.cells[row][col].get_player_id()],
                                 (row * self.rectangleSize,
                                  col * self.rectangleSize,
                                  self.rectangleSize,
                                  self.rectangleSize))
        pygame.display.update()
        self.clock.tick(60)
