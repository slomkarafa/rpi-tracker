from steering.motor.motor_unplugged import UnpluggedMotor
from steering.rider.rider_base import BaseRider


class UnpluggedRider(BaseRider):
    @classmethod
    async def init(cls, loop):
        return cls(UnpluggedMotor('left'), UnpluggedMotor('right'))
