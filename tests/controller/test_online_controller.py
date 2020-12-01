import unittest
from asyncio import Future
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock, Mock, call

from chillow.controller import OnlineController
from chillow.model.action import Action
from chillow.model.cell import Cell
from chillow.model.direction import Direction
from chillow.model.game import Game
from chillow.model.player import Player
from chillow.service.ai import PathfindingAI


# Solution to use a Mock in await expression found here: https://stackoverflow.com/a/51399767
async def async_magic():
    pass

MagicMock.__await__ = lambda x: async_magic().__await__()
mock = MagicMock()
mock.__aenter__.return_value = mock

future = Future()
future.set_result("")
mock.recv.return_value = future


def create_game(game_ended: bool):
    player1 = Player(1, 10, 10, Direction.down, 1, True, "")
    player2 = Player(2, 10, 30, Direction.down, 3, True, "")
    player3 = Player(3, 30, 10, Direction.right, 2, True, "Name 3")
    players = [player1, player2, player3]

    cells = [[Cell() for _ in range(40)] for _ in range(40)]
    for player in players:
        cells[player.y][player.x] = Cell([player])

    return Game(40, 40, cells, players, 2, game_ended, datetime(2020, 10, 1, 12, 5, 13, 0, timezone.utc))


class OnlineControllerTest(unittest.TestCase):

    @patch('websockets.connect')
    def test_online_connection_can_be_executed(self, connect_mock):
        connect_mock.return_value = mock
        view = Mock()
        data_loader = Mock()
        data_loader.load.side_effect = [create_game(True), create_game(False)]
        data_writer = Mock()
        data_writer.write.return_value = Action.get_default()
        controller = OnlineController(view, "", "", "", data_loader, data_writer, PathfindingAI.__name__, (2, 75))

        controller.play()

        view.update.assert_has_calls([call(create_game(True)), call(create_game(False))], any_order=False)
        view.end.assert_called_once()
        data_loader.load.assert_has_calls([call(""), call("")], any_order=False)
        mock.send.assert_has_calls([call(Action.get_default())])
