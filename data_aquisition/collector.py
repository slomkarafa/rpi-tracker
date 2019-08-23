import asyncio
import os
import websockets
import ujson as json
import sys
import time

sys.path.append(f'{os.path.dirname(os.path.realpath(__file__))}/../')

from odom.model import OdometerData
from odom.odometer import Odometer
from utils.files import save_json
from imu.imu_model import IMUData
from config import SERVER, SENSORS_INTERVAL
from imu import IMU
from slam import Slam
from utils.saver import Saver


class TimeGetter:
    def __init__(self):
        self.result = None

    def call(self, res):
        self.result = time.time(), res['secs'], res['nsecs']


class DataCollector:
    def __init__(self, s, i, o):
        self.saver = None
        self.imu = i
        self.slam = s
        self.trajectory_srv = self.slam.register_trajectory_service()
        self.time_srv = self.slam.register_time_service()
        self.odometer = o

    async def set_saver(self, saver):
        if not self.saver:
            self.saver = saver
            await self.saver.add('ts', IMUData.header(), OdometerData.header())

    async def del_saver(self):
        await self.saver.finish()
        self.saver = None

    async def is_saver(self):
        return bool(self.saver)

    def get_description(self):
        result = TimeGetter()
        self.time_srv(result.call)
        while not result.result:
            pass
        timers = ';'.join([str(x) for x in result.result])
        return f'system_time;ros_secs;ros_nsecs\n{timers}\n'

    @staticmethod
    def save_slam_call(path):
        def call(data):
            save_json(data, path)

        return call

    async def finish(self):
        if self.saver:
            path = self.saver.path + '/trajectory.json'
            self.trajectory_srv(self.save_slam_call(path))
            await self.del_saver()

    async def run(self):
        while True:
            if self.saver:
                try:
                    desc = self.get_description()
                    await self.saver.add_description(desc)
                    self.odometer.reset()
                    while self.saver:
                        chkpt = time.time()
                        imu_res = self.imu.get_measurements()
                        now = time.time()
                        print(f'IMu time {now - chkpt}')

                        chkpt2 = time.time()
                        odm_res = self.odometer.get_raw_counts()
                        now2 = time.time()
                        print(f'odm time {now2 - chkpt2}')

                        if self.saver:
                            await self.saver.add(now, imu_res, odm_res)
                        print(f'Data collection time: {time.time() - chkpt}')
                        await asyncio.sleep(SENSORS_INTERVAL + chkpt - time.time())
                finally:
                    if self.saver:
                        await self.del_saver()
            await asyncio.sleep(0.5)


async def main(sl, im, od):
    collector = DataCollector(sl, im, od)
    collector_future = asyncio.ensure_future(collector.run())
    uri = f"ws://{SERVER['HOST']}:{SERVER['PORT']}/collector"
    async with websockets.connect(uri) as ws:
        print('connected')
        await ws.send(json.dumps({"action": "register", "data": "sensors"}))
        while True:
            raw_resp = await ws.recv()
            resp = json.loads(raw_resp)
            if resp['action'] == 'set_saving':
                print(f'Saving switch {resp["data"]}')
                if resp['data'] and not await collector.is_saver():
                    await collector.set_saver(await Saver.create('../data/'))
                else:
                    await collector.finish()
            await ws.send(json.dumps({'action': 'saving', 'data': await collector.is_saver()}))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    imu = IMU()
    slam = Slam()
    odometer = loop.run_until_complete(Odometer.create(loop))
    loop.run_until_complete(main(slam, imu, odometer))
