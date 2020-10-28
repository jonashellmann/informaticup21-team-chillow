from dataclasses import dataclass, field
from typing import List, Type

from chillow.ai.artificial_intelligence import ArtificialIntelligence
from chillow.model.action import Action
from chillow.model.game import Game
from chillow.model.player import Player


class AlphaBetaPruningAI(ArtificialIntelligence):

    def __init__(self, player: Player, depth: int):
        super().__init__(player)
        self.depth = depth

    def create_next_action(self, game: Game) -> Action:
        root = AlphaBetaNode(game)
        raise NotImplementedError


@dataclass
class AlphaBetaNode(object):

    data: Game = None
    children: List[Type['AlphaBetaNode']] = field(default_factory=list)

    def append_child(self, node):
        self.children.append(node)
