from sanic import Sanic
from sanic.response import html, text
from sanic.websocket import WebSocketProtocol
import time
import json
import apigpio
import asyncio

from converter import circle_to_drives
from motor import Motor
from steering import Rider

app = Sanic()


async def go(request, ws):
    try:
        while True:
            data = await ws.recv()
            # print(data)
            if data == 'stop':
                await request.app.rider.stop()
            else:
                # x = list(map(int, data.strip().split(' ')))
                response = json.loads(data)

                await request.app.rider.ride(*circle_to_drives(**response))
    except Exception as e:
        print(e)
    finally:
        await request.app.rider.stop()




async def test_pwm(request):
    for x in range(0, 100, 10):
        await request.app.rider.ride(x, x)
        time.sleep(5)
    await request.app.rider.stop()
    return text('elo')



def greeting(request):
    # return html('witam sznownych panstwa')
    return html('<h1>KOCHAM KRISTINKE!!!!</h1><br/><h1>   <3<3   </h1>')


# app = Sanic()
# @app.listener('before-server-start')
# def init(_app,loop):
#     _app.rider

# def start(config, rider):
# localhost:8888

@app.listener('before_server_start')
async def init(_app, loop):
    config = app.CONFIG
    _app.pi = apigpio.Pi(_app.loop)
    print('connecting..')
    await _app.pi.connect(('localhost', 8888))
    print('connected')
    r = config['MOTORS']['RIGHT']
    l = config['MOTORS']['LEFT']

    right_motor = await Motor.create(_app.pi, r['pwm'], r['dir_0'], r['dir_1'])
    left_motor = await Motor.create(_app.pi, l['pwm'], l['dir_0'], l['dir_1'])

    _app.rider = Rider(left_motor, right_motor)
    print('init finished')

@app.listener('after_server_stop')
async def close(_app, loop):
    await _app.pi.stop()

def start(config):
    app.CONFIG = config

    app.add_websocket_route(go, '/go')
    app.add_route(greeting, '/elo')
    app.add_route(test_pwm, '/test-pwm')

    app.run('0.0.0.0', port=config['SERVER']['port'], protocol=WebSocketProtocol, debug=True)
    print('after_run')
    return app


def test():
    class TestRider():
        def ride(self, a, b):
            print(f'Ride {a}, {b}')

        def stop(self):
            print('stop')

    start({'port': 8080}, TestRider())


if __name__ == "__main__":
    test()
