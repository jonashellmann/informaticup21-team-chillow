import random

from abc import ABCMeta, abstractmethod

from src.main.python.model.action import Action


class ArtificialIntelligence(metaclass=ABCMeta):

    @abstractmethod
    def create_next_action(self, data):
        raise NotImplementedError


class ChillowAI(ArtificialIntelligence):

    def create_next_action(self, data):
        # Todo: Implement
        return random.choice(list(Action))
