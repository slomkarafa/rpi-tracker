# import RPi.GPIO as IO
import time
import apigpio

DIRECTIONS = {
    'FORWARD': (0, 1),
    'REVERSE': (1, 0),
    'STOP': (1, 1)
}


class Motor:

    def __init__(self, pi, pwm_pin, dir0_pin, dir1_pin):
        #
        # IO.setup(pwm_pin, IO.OUT)
        # IO.setup(dir0_pin, IO.OUT)
        # IO.setup(dir1_pin, IO.OUT)
        # self.pwm = IO.PWM(pwm_pin, 100)
        # self.pwm.start(0)
        self.pwm_pin = pwm_pin
        self.dir0_pin = dir0_pin
        self.dir1_pin = dir1_pin
        self.pi = pi


    @classmethod
    async def create(cls, pi, pwm_pin, dir0_pin, dir1_pin):
        await pi.set_mode(pwm_pin, apigpio.OUTPUT)
        await pi.set_mode(dir0_pin, apigpio.OUTPUT)
        await pi.set_mode(dir1_pin, apigpio.OUTPUT)
        await pi.set_PWM_dutycycle(pwm_pin, 0)
        return Motor(pi, pwm_pin, dir0_pin, dir1_pin)

    async def set_speed(self, dutycycle):
        print(f'Speed hnged to {dutycycle}')
        await self.pi.set_PWM_dutycycle(self.pwm_pin, int(dutycycle*2.55))

    async def set_direction(self, direction):
        assert direction in DIRECTIONS.keys(), f'Use one of the followings: {DIRECTIONS.keys()}'
        setup = DIRECTIONS[direction]

        await self.pi.write(self.dir0_pin, setup[0])
        await self.pi.write(self.dir1_pin, setup[1])

    async def change_direction(self):
        await self.pi.write(self.dir0_pin, not await self.pi.read(self.dir0_pin))
        await self.pi.write(self.dir1_pin, not await self.pi.read(self.dir1_pin))

    async def run(self, setting):
        direction = 'FORWARD' if setting > 0 else 'REVERSE'
        await self.set_direction(direction)
        await self.set_speed(abs(setting))
