import asyncio
import requests
import websockets
from datetime import datetime

from chillow.controller.controller import Controller
from chillow.service.data_loader import DataLoader
from chillow.service.data_writer import DataWriter
from chillow.view.view import View


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
        self.ai_class = ai_class
        self.ai_params = ai_params

    def play(self):
        asyncio.get_event_loop().run_until_complete(self.__play())
        self.monitoring.end()
        self.ai = None

    async def __play(self):
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
                    self.ai = globals()[self.ai_class](game.you, *self.ai_params)

                if game.you.active:
                    action = self.ai.create_next_action(game)
                    data_out = self.data_writer.write(action)
                    await websocket.send(data_out)
