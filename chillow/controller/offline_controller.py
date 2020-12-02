import multiprocessing
from datetime import datetime, timedelta, timezone
from random import randint

from chillow.controller.controller import Controller
from chillow.model.action import Action
from chillow.model.cell import Cell
from chillow.model.direction import Direction
from chillow.model.game import Game
from chillow.model.player import Player
from chillow.service.ai import NotKillingItselfAI, PathfindingAI, SearchTreeAI, SearchTreePathfindingAI, AIOptions
from chillow.service.ai.artificial_intelligence import ArtificialIntelligence
from chillow.service.game_service import GameService
from chillow.view.view import View


time_zone = timezone.utc


class OfflineController(Controller):

    def __init__(self, view: View):
        """Creates a new offline controller.

        Args:
            view: The UI that should be used.
        """
        super().__init__(view)
        self.__you = None
        self._game = None
        self._game_round = 0
        self._ais = []

    def play(self):
        """See base class."""
        self._create_game()
        game_service = GameService(self._game, ignore_deadline=False)

        self._view.update(self._game)

        while self._game.running:
            self._game_round += 1
            time_to_react = randint(4, 16)
            self.__reset_game_deadline(time_to_react)

            # Read input from user if there is a human player
            action = None
            if self.__you is not None:
                action = self._view.read_next_action()
                if datetime.now(time_zone) > self._game.deadline:
                    action = Action.get_default()
                self.__reset_game_deadline(time_to_react)

            for ai in self._ais:
                if ai is not None and ai.player.active:
                    action = self.__choose_ai_action(ai, time_to_react)
                    game_service.do_action(ai.player, action)
                    self.__reset_game_deadline(time_to_react)

            # Perform action of human player after AIs finished their calculations
            if self.__you is not None:
                game_service.do_action(self.__you, action)

            self._view.update(self._game)

    def _create_game(self) -> None:
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

        self._game = Game(width, height, cells, players, 1, True, datetime.now(time_zone))
        self._game_round = 0

        self.__you = None
        ai0 = NotKillingItselfAI(player1, [AIOptions.max_distance], 1, 0, 3)
        # Comment out next two lines if you want to play on your own.
        # self.__you = player1
        # ai0 = None

        ai1 = PathfindingAI(player2, 2, 75)
        ai2 = SearchTreePathfindingAI(player3, 2, 75, 2)
        ai3 = SearchTreeAI(player4, 2)

        self._ais = [ai0, ai1, ai2, ai3]

    def _log_execution_time(self, ai: ArtificialIntelligence, execution_time: float):
        pass

    def __reset_game_deadline(self, time_to_react: int):
        self._game.deadline = datetime.now(time_zone) + timedelta(0, time_to_react)

    def __choose_ai_action(self, ai: ArtificialIntelligence, time_to_react: int) -> Action:
        return_value = multiprocessing.Value('i', Action.get_default().get_index())

        process = multiprocessing.Process(target=Controller.call_ai, args=(ai, self._game.copy(), return_value,))
        start = datetime.now(time_zone)
        process.start()
        process.join(time_to_react - 1)  # wait time_to_react seconds minus one for the calculation to be finished

        if process.is_alive():
            # If an execution is terminated, the execution time is set to 1 minute.
            start = datetime.now(time_zone) - timedelta(seconds=60)
            process.terminate()

        self._log_execution_time(ai, (datetime.now(time_zone) - start).total_seconds())
        return Action.get_by_index(return_value.value)
