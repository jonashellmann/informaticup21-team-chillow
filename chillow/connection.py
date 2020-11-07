import asyncio
import os
import requests
from datetime import datetime, timedelta
import websockets

from abc import ABCMeta, abstractmethod

from chillow.ai.not_killing_itself_ai import NotKillingItselfAI, AIOptions
from chillow.ai.pathfinding_ai import PathfindingAI
from chillow.ai.pathfinding_search_tree_ai import PathfindingSearchTreeAI
from chillow.ai.search_tree_ai import SearchTreeAI
from chillow.service.data_loader import JSONDataLoader
from chillow.service.data_writer import JSONDataWriter
from chillow.ai.random_ai import RandomWaitingAI
from chillow.service.game_service import GameService
from chillow.controller.monitoring import GraphicalMonitoring, ConsoleMonitoring
from chillow.model.game import Game
from chillow.model.player import Player
from chillow.model.direction import Direction
from chillow.model.cell import Cell


class Connection(metaclass=ABCMeta):

    def __init__(self):
        if not os.getenv("DEACTIVATE_PYGAME", False):
            self.monitoring = GraphicalMonitoring()
        else:
            self.monitoring = ConsoleMonitoring()

    @abstractmethod
    def play(self):
        raise NotImplementedError


class OnlineConnection(Connection):

    def __init__(self):
        super().__init__()
        self.url = os.environ["URL"]
        self.time_url = self.url.replace("wss://", "https://") + "_time"
        self.key = os.environ["KEY"]
        self.data_loader = JSONDataLoader()
        self.data_writer = JSONDataWriter()
        self.ai = None

    def play(self):
        asyncio.get_event_loop().run_until_complete(self._play())
        self.monitoring.end()

    async def _play(self):
        async with websockets.connect(f"{self.url}?key={self.key}") as websocket:
            while True:
                game_data = await websocket.recv()
                game = self.data_loader.load(game_data)

                time_data = requests.get(self.time_url).text
                server_time = self.data_loader.read_server_time(time_data)
                own_time = datetime.now(server_time.tzinfo).replace(microsecond=0)
                game.normalize_deadline(server_time, own_time)

                self.monitoring.update(game)

                if self.ai is None:
                    self.ai = RandomWaitingAI(game.you)

                if game.you.active:
                    action = self.ai.create_next_action(game)
                    data_out = self.data_writer.write(action)
                    await websocket.send(data_out)


class OfflineConnection(Connection):

    def __init__(self):
        super().__init__()

    def play(self):
        player1 = Player(1, 5, 5, Direction.down, 1, True, "Human Player 1")
        player2 = Player(2, 25, 5, Direction.down, 1, True, "AI Player 1")
        player3 = Player(3, 5, 15, Direction.up, 1, True, "AI Player 2")
        player4 = Player(4, 25, 15, Direction.up, 1, True, "AI Player 4")
        players = [player1, player2, player3, player4]
        height = 20
        width = 30
        cells = [[Cell() for _ in range(width)] for _ in range(height)]
        cells[player1.y][player1.x] = Cell([player1])
        cells[player2.y][player2.x] = Cell([player2])
        cells[player3.y][player3.x] = Cell([player3])
        cells[player4.y][player4.x] = Cell([player4])
        game = Game(width, height, cells, players, 1, True, datetime.now() + timedelta(0, 180))

        self.monitoring.update(game)

        game_service = GameService(game)
        ai0 = PathfindingAI(player1, 2, 75)
        ai1 = NotKillingItselfAI(player2, game, [AIOptions.max_distance], 1, 0)
        ai2 = PathfindingSearchTreeAI(player3, 2, 75, 2)
        ai3 = SearchTreeAI(player4, 2)
        ais = [ai0, ai1, ai2, ai3]

        while game.running:
            # if player1.active:
            #     action = self.monitoring.create_next_action()
            #     game_service.do_action(player1, action)

            for ai in ais:
                if ai.player.active:
                    action = ai.create_next_action(game.copy())
                    game_service.do_action(ai.player, action)

            self.monitoring.update(game)
