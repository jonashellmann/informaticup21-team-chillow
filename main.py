import os
import logging

from chillow.connection import OnlineConnection, OfflineConnection


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.WARNING)

if not os.getenv('PLAY_ONLINE', False):
    con = OfflineConnection()
else:
    con = OnlineConnection()
con.play()
