import os

from chillow.connection import OnlineConnection, OfflineConnection


if not os.getenv('PLAY_ONLINE', False):
    con = OfflineConnection()
else:
    con = OnlineConnection()
con.play()
