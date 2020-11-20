import asyncio
import requests
import websockets
import multiprocessing
from datetime import datetime

from chillow.controller.controller import Controller
from chillow.model.action import Action
from chillow.model.game import Game
from chillow.service.ai.artificial_intelligence import ArtificialIntelligence
from chillow.model.action import ActionValue
from chillow.service.data_loader import DataLoader
from chillow.service.data_writer import DataWriter
from chillow.view.view import View
from chillow.service.ai import *


class OnlineController(Controller):

    def __init__(self, monitoring: View, url: str, key: str, data_loader: DataLoader, data_writer: DataWriter,
                 ai_class: str, ai_params):
        super().__init__(monitoring)
        self.url = url
        self.time_url = self.url.replace("wss://", "https://") + "_time"
        self.key = key
        self.data_loader = data_loader
        self.data_writer = data_writer
        self.ai = None
        self.default_ai = None
        self.ai_class = ai_class
        self.ai_params = ai_params

    def play(self):
        asyncio.get_event_loop().run_until_complete(self.__play())
        self.monitoring.end()
        self.ai = None
        self.default_ai = None

    async def __play(self):
        async with websockets.connect(f"{self.url}?key={self.key}") as websocket:
            while True:
                game_data = await websocket.recv()
                game = self.data_loader.load(game_data)

                self.monitoring.update(game)

                if not game.running:
                    break

                time_data = requests.get(self.time_url).text
                server_time = self.data_loader.read_server_time(time_data)
                own_time = datetime.now(server_time.tzinfo)
                game.normalize_deadline(server_time, own_time)

                if self.ai is None:
                    self.ai = globals()[self.ai_class](game.you, *self.ai_params)
                    self.default_ai = NotKillingItselfAI(game.you, [AIOptions.max_distance], 1, 0)

                if game.you.active:
                    action = self.__choose_action(game, server_time.tzinfo)
                    data_out = self.data_writer.write(action)
                    await websocket.send(data_out)

    def __choose_action(self, game: Game, timezone: datetime.tzinfo) -> Action:
        return_value = ActionValue()
        self.default_ai.create_next_action(game, return_value)

        own_time = datetime.now(timezone)
        seconds_for_calculation = (game.deadline - own_time).seconds

        process = multiprocessing.Process(target=OnlineController.call_ai, args=(self.ai, game, return_value,))
        process.start()
        process.join(seconds_for_calculation - 1)

        if process.is_alive():
            process.terminate()

        return return_value.action

    @staticmethod
    def call_ai(ai: ArtificialIntelligence, game: Game, return_value: ActionValue):
        ai.create_next_action(game, return_value)
