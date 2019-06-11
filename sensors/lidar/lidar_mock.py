import asyncio
import ujson as json
from sensors.lidar.lidar_base import BaseLidar


class MockLidar(BaseLidar):

    async def run(self):
        while True:
            print('I am fully working lidar')
            await asyncio.sleep(5)
            print(self.listener)
            if self.listener:
                msg = json.dumps({
                    'data': bytearray(200 * 200),
                    'dim': 200
                })
                await self.listener(msg)
