import asyncio
import requests
import websockets
import multiprocessing
from datetime import datetime, timezone
from requests import RequestException

from chillow.controller.controller import Controller
from chillow.model.action import Action
from chillow.model.game import Game
from chillow.service.data_loader import DataLoader
from chillow.service.data_writer import DataWriter
from chillow.view.view import View
from chillow.service.ai import *


class OnlineController(Controller):

    def __init__(self, view: View, url: str, key: str, server_time_url: str, data_loader: DataLoader,
                 data_writer: DataWriter, ai_class: str, ai_params):
        """Creates a new online controller.

        Args:
            view: The UI that should be used.
            url: The URL of the spe_ed server.
            key: The API key.
            server_time_url: The URL to request the current time of the server.
            data_loader: Object to load data.
            data_writer: Object to write data.
            ai_class: The name of the AI class to be used.
            ai_params: The parameters of the AI.
        """

        super().__init__(view)
        self.__url = url
        self.__key = key
        self.__server_time_url = server_time_url
        self.__data_loader = data_loader
        self.__data_writer = data_writer
        self.__ai = None
        self.__default_ai = None
        self.__ai_class = ai_class
        self.__ai_params = ai_params

    def play(self):
        """See base class."""
        asyncio.get_event_loop().run_until_complete(self.__play())
        self._view.end()
        self.__ai = None
        self.__default_ai = None

    async def __play(self):
        async with websockets.connect(f"{self.__url}?key={self.__key}") as websocket:
            while True:
                game_data = await websocket.recv()
                game = self.__data_loader.load(game_data)

                self._view.update(game)

                if not game.running:
                    break

                try:
                    time_data = requests.get(self.__server_time_url).text
                    server_time = self.__data_loader.read_server_time(time_data)
                except (RequestException, ValueError):
                    server_time = datetime.now(timezone.utc)
                own_time = datetime.now(server_time.tzinfo)
                game.normalize_deadline(server_time, own_time)

                if self.__ai is None:
                    self.__ai = globals()[self.__ai_class](game.you, *self.__ai_params)
                    self.__default_ai = NotKillingItselfAI(game.you, [AIOptions.max_distance], 1, 0, 3)

                if game.you.active:
                    action = self.__choose_action(game, server_time.tzinfo)
                    data_out = self.__data_writer.write(action)
                    await websocket.send(data_out)

    def __choose_action(self, game: Game, time_zone: datetime.tzinfo) -> Action:
        return_value = multiprocessing.Value('i')
        self.__default_ai.create_next_action(game, return_value)

        own_time = datetime.now(time_zone)
        seconds_for_calculation = (game.deadline - own_time).seconds

        process = multiprocessing.Process(target=Controller.call_ai, args=(self.__ai, game, return_value,))
        process.start()
        process.join(seconds_for_calculation - 1)

        if process.is_alive():
            process.terminate()

        return Action.get_by_index(return_value.value)
