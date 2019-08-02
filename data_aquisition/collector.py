import asyncio
import os
import websockets
import ujson as json
import sys
import time

sys.path.append('../')

from config import SERVER
from imu import IMU
from slam import Slam
from utils.saver import Saver


class DataCollector:
    def __init__(self):
        self.saver = None

    async def set_saver(self, saver):
        if not self.saver:
            self.saver = saver

    async def del_saver(self):
        self.saver.finish()
        self.saver = None

    async def is_saver(self):
        return bool(self.saver)

    async def run(self):
        try:
            imu = IMU()
            slam_pose = Slam().pose_caller()
            while True:
                chkpt = time.time()
                imu_res = imu.get_measurements()
                slam_res = slam_pose()
                if self.saver:
                    self.saver.add(imu_res, slam_res)
                print(f'Data collection time: {time.time() - chkpt}')
                await asyncio.sleep(0.1)
        finally:
            if self.saver:
                self.saver.finish()


async def main():
    collector = DataCollector()
    collector_future = asyncio.ensure_future(collector.run())
    uri = f"ws://{SERVER['HOST']}:{SERVER['PORT']}"
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({"action": "register", "data": "sensors"}))
        while True:
            raw_resp = await ws.recv()
            resp = json.loads(raw_resp)
            if resp['action'] == 'set_saving':
                if resp['data']:
                    await collector.set_saver(Saver('./'))
                else:
                    await collector.del_saver()
            await ws.send(json.dumps({'action': 'saving', 'data': collector.is_saver()}))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
