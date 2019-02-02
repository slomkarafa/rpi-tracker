from sanic import Sanic
from sanic.response import html
from sanic.websocket import WebSocketProtocol
import time
import json

# def go(request):
#     dir = request.get('dir')
#     if not dir:
#         return html('no direcrion in request')
#     print(f'going {dir}')
#     if dir == STEERING.GO:
#         while True:
#             cmd = await request.stream.get()
#             assert cmd in STEERING.values(), f'{cmd} is wrong cmmand, use one of following: {STEERING.values()}'
#
#             if cmd is STEERING.SP:
#                 break
#             print(cmd)
from converter import circle_to_drives


def get_go_func(rider):
    async def go(request, ws):
        try:
            while True:
                data = await ws.recv()
                # print(data)
                if data == 'stop':
                    rider.stop()
                else:
                    # x = list(map(int, data.strip().split(' ')))
                    response = json.loads(data)

                    rider.start(*circle_to_drives(**response))
        except Exception as e:
            print(e)
        finally:
            rider.stop()

    return go


def get_start_func(rider):
    async def start(request):
        print('riding')
        rider.ride(100, 100)

    return start


def get_stop_func(rider):
    async def stop(request):
        print('stop')
        rider.stop()

    return stop


def greeting(request):
    # return html('witam sznownych panstwa')
    return html('<h1>KOCHAM KRISTINKE!!!!</h1><br/><h1>   <3<3   </h1>')


def init(config, rider):
    app = Sanic()
    # app.add_route(get_start_func(rider), '/start', methods=['PUT'])
    # app.add_route(get_stop_func(rider), '/stop', methods=['PUT'])

    app.add_websocket_route(get_go_func(rider), '/go')
    app.add_route(greeting, '/elo')

    app.run('0.0.0.0', port=config['port'], protocol=WebSocketProtocol, debug=True)
    return app


def test():
    class TestRider():
        def start(self, a, b):
            print(f'Ride {a}, {b}')

        def stop(self):
            print('stop')

    init({'port': 8080}, TestRider())


if __name__ == "__main__":
    test()
