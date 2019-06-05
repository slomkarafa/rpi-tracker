import asyncio

from sensors.lidar.lidar_base import BaseLidar


class MockLidar(BaseLidar):

    async def run(self):
        while True:
            print('I am fully working lidar')
            await asyncio.sleep(5)
            print(self.listener)
            if self.listener:
                await self.listener(bytearray(200 * 200))
