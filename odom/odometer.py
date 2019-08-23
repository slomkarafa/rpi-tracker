import apigpio
import asyncio
import os
import sys

sys.path.append(f'{os.path.dirname(os.path.realpath(__file__))}/../')

from odom.encoder import Encoder
from odom.model import OdometerData
from config import ENCODERS, PIGPIO


class Odometer:
    def __init__(self, left, right):
        self.l = left
        self.r = right

    def get_raw_counts(self):
        return OdometerData(self.l.count, self.r.count)

    def reset(self):
        self.r.reset()
        self.l.reset()

    @classmethod
    async def create(cls, loop):
        pi = apigpio.Pi(loop)
        print('connecting..')
        await pi.connect((PIGPIO['HOST'], PIGPIO['PORT']))
        print('pigpio connected')
        right_enc = await Encoder.create(pi, ENCODERS['RIGHT'])
        left_enc = await Encoder.create(pi, ENCODERS['LEFT'])
        return cls(left_enc, right_enc)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    od = loop.run_until_complete(Odometer.create(loop))

    loop.run_forever()
