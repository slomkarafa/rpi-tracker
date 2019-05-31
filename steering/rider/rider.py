from config import PIGPIO, MOTORS
from steering.motor.motor import Motor
from steering.rider.rider_base import BaseRider

import apigpio


class Rider(BaseRider):

    @classmethod
    async def init(cls, loop):
        pi = apigpio.Pi(loop)
        print('connecting..')
        await pi.connect((PIGPIO['HOST'], PIGPIO['PORT']))
        print('connected')
        right_motor = await Motor.create(pi, MOTORS['RIGHT'])
        left_motor = await Motor.create(pi, MOTORS['LEFT'])

        return cls(left_motor, right_motor)
