from abc import ABC, abstractmethod


class MotorI(ABC):

    @abstractmethod
    async def set_speed(self, dutycycle):
        ...

    @abstractmethod
    async def set_direction(self, direction):
        ...

    @abstractmethod
    async def change_direction(self):
        ...

    @abstractmethod
    async def run(self, setting):
        ...
