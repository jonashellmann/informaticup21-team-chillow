from dataclasses import dataclass, field
from typing import List, Type

from chillow.model.action import Action
from chillow.model.game import Game


@dataclass
class AlphaBetaRoot(object):
    __game: Game
    __children: List[Type['AlphaBetaNode']] = field(default_factory=list, init=False)

    def get_children(self, depth: int):
        if depth <= 0:
            return [self]

        result = []
        for child in self.__children:
            for grandchild in child.get_children(depth - 1):
                result.append(grandchild)
        return result

    def append_child(self, node):
        self.__children.append(node)

    # Todo: Anpassen
    def evaluate(self) -> int:
        if not self.__game.you.active:
            return 0

        evaluation = 1
        for child in self.__children:
            evaluation += child.evaluate()
        return evaluation

    # Todo: Anpassen für weitere Tiefen im Baum
    def get_winning_action(self) -> Action:
        for child in self.__children:
            if child.evaluate() > 0:
                return child.get_action()


@dataclass
class AlphaBetaNode(AlphaBetaRoot):
    __action: Action

    def get_action(self):
        return self.__action
