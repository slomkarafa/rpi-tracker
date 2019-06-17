import uvloop
import asyncio

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
import json

from converter import circle_to_drives


def sender(ws):
    async def send(msg):
        # await ws.send(msg)
        print('elo')

    return send


async def go(request, ws):
    try:
        # request.app.slam.subscribe(sender(ws))
        while True:
            data = await ws.recv()
            print(data)
            if data == 'stop':
                await request.app.rider.stop()
            else:
                # x = list(map(int, data.strip().split(' ')))
                response = json.loads(data)

                await request.app.rider.ride(*circle_to_drives(**response))
    except Exception as e:
        print(e)
    finally:
        request.app.lidar.unsunscibe()
        await request.app.rider.stop()
