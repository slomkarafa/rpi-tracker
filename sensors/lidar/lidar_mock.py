import asyncio

import ujson as json
# import json

from sensors.lidar.lidar_base import BaseLidar

DATA = [137, 80, 78, 71, 13, 10, 26, 10, 0, 0, 0, 13, 73, 72, 68, 82, 0, 0, 1, 140, 0, 0, 1, 34, 4, 3, 0, 0, 0, 24, 1,
        248, 231, 0, 0, 0, 21, 80, 76, 84, 69, 255, 255, 255, 0, 0, 0, 220, 217, 207, 0, 100, 0, 176, 196, 222, 0, 153,
        204, 204, 255, 255, 227, 179, 150, 92, 0, 0, 1, 29, 73, 68, 65, 84, 120, 156, 237, 207, 1, 13, 128, 64, 12, 4,
        193, 211, 130, 5, 44, 96, 1, 11, 248, 151, 192, 91, 104, 66, 66, 191, 153, 85, 176, 147, 99, 68, 249, 123, 224,
        155, 48, 58, 181, 24, 217, 62, 140, 78, 205, 98, 156, 165, 146, 171, 84, 114, 151, 74, 158, 82, 24, 24, 24, 24,
        24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24,
        24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24,
        24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24,
        24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24,
        24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24,
        24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24,
        24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24,
        24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 157, 25, 187, 135, 209, 169, 73, 140, 9, 97, 116, 106, 8, 227, 5, 178,
        0, 69, 109, 104, 207, 36, 38, 0, 0, 0, 0, 73, 69, 78, 68, 174, 66, 96, 130]

TEST_DATA = json.dumps({
    # "data": str(bytes(200 * 200)),
    "data": bytearray(DATA),
    'dim': 200
})


class MockLidar(BaseLidar):

    async def run(self):
        while True:
            print('I am fully working lidar')
            await asyncio.sleep(5)
            print(self.listener)
            if self.listener:
                await self.listener(TEST_DATA)
