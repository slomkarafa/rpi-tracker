from sanic import Sanic
from sanic.response import html, text
from sanic.websocket import WebSocketProtocol
import time
import json

from converter import circle_to_drives

from config import SERVER

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


async def init(_app, loop):
    _app.rider = await Rider.init(loop)
    print('init finished')


@app.listener('after_server_stop')
async def close(_app, loop):
    await _app.pi.stop()


def run():
    app.register_listener(init, 'before_server_start')
    app.add_websocket_route(go, '/go')
    app.add_route(greeting, '/elo')
    app.add_route(test_pwm, '/test-pwm')

    app.run('0.0.0.0', port=SERVER['port'], protocol=WebSocketProtocol, debug=True)
    print('after_run')
    return app
