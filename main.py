import os
import logging
import argparse

from chillow.service.ai import *
from chillow.controller import OnlineController, OfflineController, AIEvaluationController
from chillow.service.data_loader import JSONDataLoader
from chillow.service.data_writer import JSONDataWriter

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.WARNING)

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--play-online', type=bool, default=False)
    parser.add_argument('-d', '--deactivate-pygame', type=bool, default=False)
    parser.add_argument('-r', '--ai-eval-runs', type=int, default=0)
    parser.add_argument('-p', '--ai-eval-db-path', type=str, default="evaluation.db")
    args = parser.parse_args()

    if args.deactivate_pygame:
        from chillow.view.console_view import ConsoleView
        monitoring = ConsoleView()
    else:
        from chillow.view.graphical_view import GraphicalView
        monitoring = GraphicalView()

    if not args.play_online:
        if args.ai_eval_runs > 0:
            con = AIEvaluationController(args.ai_eval_runs, args.ai_eval_db_path)
        else:
            con = OfflineController(monitoring)
    else:
        url = os.environ["URL"]
        key = os.environ["KEY"]
        data_loader = JSONDataLoader()
        data_writer = JSONDataWriter()
        ai_class = PathfindingAI.__name__
        ai_params = (2, 75)

        con = OnlineController(monitoring, url, key, data_loader, data_writer, ai_class, ai_params)

    con.play()
