import RPi.GPIO as IO
import time

DIRECTIONS = {
    'FORWARD': (0, 1),
    'REVERSE': (1, 0),
    'STOP': (1, 1)
}


class Motor:

    def __init__(self, pwm_pin, dir0_pin, dir1_pin):
        IO.setwarnings(False)
        IO.setmode(IO.BCM)
        IO.setup(pwm_pin, IO.OUT)
        IO.setup(dir0_pin, IO.OUT)
        IO.setup(dir1_pin, IO.OUT)
        self.pwm = IO.PWM(pwm_pin, 100)
        self.pwm.start(0)
        self.dir0_pin = dir0_pin
        self.dir1_pin = dir1_pin

    def set_speed(self, dutycycle):
        self.pwm.ChangeDutyCycle(dutycycle)

    def set_direction(self, direction):
        assert direction in DIRECTIONS.keys(), f'Use one of the followings: {DIRECTIONS.keys()}'
        setup = DIRECTIONS[direction]
        IO.output(self.dir0_pin, setup[0])
        IO.output(self.dir1_pin, setup[1])

    def change_direction(self):
        IO.output(self.dir0_pin, not IO.input(self.dir0_pin))
        IO.output(self.dir1_pin, not IO.input(self.dir1_pin))

    def run(self, setting):
        direction = 'FORWARD' if setting > 0 else 'REVERSE'
        self.set_direction(direction)
        self.set_speed(abs(setting))
