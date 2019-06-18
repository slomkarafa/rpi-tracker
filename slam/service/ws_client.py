import ujson as json
# import json

from websocket import create_connection


from service.service import ServiceI


class WebsocketService(ServiceI):
    def __init__(self):
        self.ws = create_connection('ws://localhost:8080/slam')

    def send(self, msg):
        self.ws.send(json.dumps({'action': 'map', 'data': msg}))

    def recv(self, msg):
        pass

