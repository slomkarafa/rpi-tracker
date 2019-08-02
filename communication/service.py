import asyncio
import os
import websockets
import ujson as json
import sys

sys.path.append(f'{os.path.dirname(os.path.realpath(__file__))}/../')

from steering import Rider

loop = asyncio.get_event_loop()
queue = asyncio.Queue(loop=loop)
registered = {
    "app": set(),
    "sensors": set()
}

rider = loop.run_until_complete(Rider.init(loop))


async def handle_map(ws, data):
    try:
        if registered['app']:
            await asyncio.wait([ws.send(bytes(data)) for ws in registered['app']])
            pass
    except Exception as e:
        print(e)
        # registered.remove(ws)


async def handle_manual_go(ws, data):
    if data == 'stop':
        await rider.stop()
    else:
        if abs(data['right']) > 100 or abs(data['left']) > 100:
            print('ERROR KURWA')
        await rider.ride(data.get('left', 0), data.get('right', 0))


async def register(ws, data):
    print('registering ')
    registered[data].add(ws)
    if data == 'app':
        await is_saving(ws, data)


async def set_saving(ws, data):
    await asyncio.wait([ws.send(json.dumps({'action': 'set_saving', 'data': data})) for ws in registered['sensors']])


async def is_saving(ws, data):
    await asyncio.wait([ws.send(json.dumps({'action': 'is_saving'})) for ws in registered['sensors']])


async def saving(ws, data):
    await asyncio.wait([ws.send(json.dumps({'action': 'saving', 'data': data})) for ws in registered['app']])


async def que_producer(msg):
    await queue.put(msg)


async def consumer(msg, ws):
    msg = json.loads(msg)
    action = msg.get('action', '')
    fn = {
        'map': handle_map,
        'manual': handle_manual_go,
        'register': register,
        'set_saving': set_saving,
        'is_saving': is_saving,
        'saving': saving
    }.get(action)
    if fn:
        await fn(ws, msg.get('data'))


async def producer(queue):
    while True:
        return await queue.get()


async def consumer_handler(websocket, path):
    print(path)
    async for message in websocket:
        await consumer(message, websocket)


async def producer_handler(websocket, path):
    while True:
        message = await producer(queue)
        await websocket.send(message)


async def handler(websocket, path):
    consumer_task = asyncio.ensure_future(
        consumer_handler(websocket, path))
    producer_task = asyncio.ensure_future(
        producer_handler(websocket, path))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()


start_server = websockets.serve(handler, '0.0.0.0', 8080)

loop.run_until_complete(start_server)
loop.run_forever()
