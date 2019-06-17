import asyncio
import sys

import requests
import rpyc

sys.path.append('../')

from communication.server import create
from config import DISTRIBUTED, SERVER
#
#
# class MapModel:
#     def __init__(self):
#         self.map = bytes()
#
#     def update(self, new_map):
#         self.map = new_map
#
#     def get(self):
#         return self.map
#
#
# map_bytes = MapModel()
#
#


class RestService(rpyc.Service):
    def on_connect(self, conn):
        # code that runs when a connection is created
        # (to init the service, if needed)
        pass

    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        # (to finalize the service, if needed)
        pass

    def exposed_update_map(self, map):
        requests.post(f'0.0.0.0:{SERVER["port"]}/send-map', data=map)

    def get_question(self):  # while this method is not exposed
        return "what is the airspeed velocity of an unladen swallow?"


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer

    server = create()
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(server)

    t = ThreadedServer(RestService, port=DISTRIBUTED['REST'])
    t.start()

    loop.run_forever()
#
#
# class ELO:
#