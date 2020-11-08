import os
import logging

from chillow.connection import OnlineConnection, OfflineConnection
from chillow.service.data_loader import JSONDataLoader
from chillow.service.data_writer import JSONDataWriter

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.WARNING)

if not os.getenv('PLAY_ONLINE', False):
    con = OfflineConnection()
else:
    url = os.environ["URL"]
    key = os.environ["KEY"]
    data_loader = JSONDataLoader()
    data_writer = JSONDataWriter()

    con = OnlineConnection(url, key, data_loader, data_writer)

con.play()
