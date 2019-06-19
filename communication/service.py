import asyncio
import websockets
import ujson as json
import sys

sys.path.append('../')

from steering import Rider

loop = asyncio.get_event_loop()
queue = asyncio.Queue(loop=loop)
registered = set()

rider = loop.run_until_complete(Rider.init(loop))


async def handle_map(data):
    try:
        if registered:
            await asyncio.wait([ws.send(bytes(data)) for ws in registered])
            pass
    except Exception as e:
        print(e)
        # registered.remove(ws)


async def handle_manual_go(data):
    if data == 'stop':
        await rider.stop()
    else:
        if abs(data['right'])>100 or abs(data['left'])>100:
            print('ERROR KURWA')
        await rider.ride(data.get('left', 0), data.get('right', 0))


async def register_for_map(ws):
    print('registering for map')
    registered.add(ws)


async def que_producer(msg):
    await queue.put(msg)


async def consumer(msg, ws):
    msg = json.loads(msg)
    action = msg.get('action', '')
    if action == 'register_for_map':
        await register_for_map(ws)
        return
    fn = {
        'map': handle_map,
        'manual': handle_manual_go
    }.get(action)
    if fn:
        await fn(msg.get('data'))


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
