import os
import logging

from chillow.ai import *
from chillow.connection import OnlineConnection, OfflineConnection
from chillow.controller.monitoring import GraphicalMonitoring, ConsoleMonitoring
from chillow.service.data_loader import JSONDataLoader
from chillow.service.data_writer import JSONDataWriter

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.WARNING)

if not os.getenv("DEACTIVATE_PYGAME", False):
    monitoring = GraphicalMonitoring()
else:
    monitoring = ConsoleMonitoring()

if not os.getenv('PLAY_ONLINE', False):
    con = OfflineConnection(monitoring)
else:
    url = os.environ["URL"]
    key = os.environ["KEY"]
    data_loader = JSONDataLoader()
    data_writer = JSONDataWriter()
    ai_class = PathfindingAI.__name__
    ai_params = (2, 75)

    con = OnlineConnection(monitoring, url, key, data_loader, data_writer, ai_class, ai_params)

con.play()
