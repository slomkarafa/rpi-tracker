from sanic import Sanic
from sanic.response import html
from sanic.websocket import WebSocketProtocol
import time
import json

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

                    rider.ride(*circle_to_drives(**response))
        except Exception as e:
            print(e)
        finally:
            rider.stop()

    return go


def get_pwm_tester(rider):
    async def test_pwm(requet):
        for x in range(0, 100, 10):
            rider.ride(x, x)
            time.sleep(5)

    return test_pwm


def greeting(request):
    # return html('witam sznownych panstwa')
    return html('<h1>KOCHAM KRISTINKE!!!!</h1><br/><h1>   <3<3   </h1>')


def init(config, rider):
    app = Sanic()

    app.add_websocket_route(get_go_func(rider), '/go')
    app.add_route(greeting, '/elo')
    app.add_route(get_pwm_tester(rider), '/test-pwm')

    app.run('0.0.0.0', port=config['port'], protocol=WebSocketProtocol, debug=True)
    return app


def test():
    class TestRider():
        def ride(self, a, b):
            print(f'Ride {a}, {b}')

        def stop(self):
            print('stop')

    init({'port': 8080}, TestRider())


if __name__ == "__main__":
    test()
