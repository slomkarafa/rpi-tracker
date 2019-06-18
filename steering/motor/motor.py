import apigpio

from steering.motor.motor_interface import MotorI

DIRECTIONS = {
    'FORWARD': (0, 1),
    'REVERSE': (1, 0),
    'STOP': (1, 1)
}


class Motor(MotorI):

    def __init__(self, pi, pwm_pin, dir0_pin, dir1_pin):
        # super().__init__(pi, pwm_pin, dir0_pin, dir1_pin)
        self.pwm_pin = pwm_pin
        self.dir0_pin = dir0_pin
        self.dir1_pin = dir1_pin
        self.pi = pi

    @classmethod
    async def create(cls, pi, config):
        pwm_pin = config['pwm']
        dir0_pin = config['dir_0']
        dir1_pin = config['dir_1']
        await pi.set_mode(pwm_pin, apigpio.OUTPUT)
        await pi.set_mode(dir0_pin, apigpio.OUTPUT)
        await pi.set_mode(dir1_pin, apigpio.OUTPUT)
        await pi.set_PWM_dutycycle(pwm_pin, 0)
        return Motor(pi, pwm_pin, dir0_pin, dir1_pin)

    async def set_speed(self, dutycycle):
        await self.pi.set_PWM_dutycycle(self.pwm_pin, int(dutycycle * 2.55))

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
