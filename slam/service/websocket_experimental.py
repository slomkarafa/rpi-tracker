# from slam.service.service import ServiceI
#
#
# class WebsocketService(ServiceI):
#     def __init__(self):
#
#     def send(self, msg):
#         pass
#
#     def recv(self, msg):
#         pass

import asyncio
import threading
import websockets
import json


class WSClient(threading.Thread):

    def __init__(self):
        super().__init__()
        self._loop = None
        self._tasks = {}
        self._stop_event = None

    def run(self):
        self._loop = asyncio.new_event_loop()
        self._stop_event = asyncio.Event(loop=self._loop)
        try:
            self._loop.run_until_complete(self._stop_event.wait())
            self._loop.run_until_complete(self._clean())
        finally:
            self._loop.close()

    def stop(self):
        self._loop.call_soon_threadsafe(self._stop_event.set)

    def subscribe(self, url, sub_msg, callback):
        def _subscribe():
            if url not in self._tasks:
                task = self._loop.create_task(
                    self._listen(url, sub_msg, callback))
                self._tasks[url] = task

        self._loop.call_soon_threadsafe(_subscribe)

    def unsubscribe(self, url):
        def _unsubscribe():
            task = self._tasks.pop(url, None)
            if task is not None:
                task.cancel()

        self._loop.call_soon_threadsafe(_unsubscribe)

    async def _listen(self, url, sub_msg, callback):
        try:
            while not self._stop_event.is_set():
                try:
                    ws = await websockets.connect(url, loop=self._loop)
                    await ws.send(json.dumps(sub_msg))
                    async for data in ws:
                        data = json.loads(data)

                        # NOTE: please make sure that `callback` won't block,
                        # and it is allowed to update GUI from threads.
                        # If not, you'll need to find a way to call it from
                        # main/GUI thread (similar to `call_soon_threadsafe`)
                        callback(data)
                except Exception as e:
                    print('ERROR; RESTARTING SOCKET IN 2 SECONDS', e)
                    await asyncio.sleep(2, loop=self._loop)
        finally:
            self._tasks.pop(url, None)

    async def _clean(self):
        for task in self._tasks.values():
            task.cancel()
        await asyncio.gather(*self._tasks.values(), loop=self._loop)
