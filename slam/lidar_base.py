import asyncio
from abc import ABC, abstractmethod
from contextlib import suppress


class BaseLidar(ABC):

    def __init__(self, on_map_change):
        self.listener = None
        self.map_listener = on_map_change

    # async def stop(self):
    #     if self.task:
    #         self.task.cancel()
    #         with suppress(asyncio.CancelledError):
    #             await self.task

    def start(self):
        self.run()

    @abstractmethod
    def run(self):
        ...

    def subscribe(self, fn):
        print('subscribed')
        self.listener = fn

    def unsubscribe(self):
        self.listener = None
