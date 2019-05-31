from steering.motor.motor_interface import MotorI


class UnpluggedMotor(MotorI):
    def __init__(self, name):
        self.name = name

    async def set_speed(self, dutycycle):
        print(f'{self.name} motor - set_speed: {dutycycle}')

    async def set_direction(self, direction):
        print(f'{self.name} motor - set_direction: {direction}')

    async def change_direction(self):
        print(f'{self.name} motor - change_direction')

    async def run(self, setting):
        print(f'{self.name} motor - run!: {setting}')