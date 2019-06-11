import asyncio
from abc import ABC, abstractmethod
from contextlib import suppress


class BaseLidar(ABC):

    def __init__(self):
        self.listener = None
        self.task = None

    async def stop(self):
        if self.task:
            self.task.cancel()
            with suppress(asyncio.CancelledError):
                await self.task

    async def start(self):
        if not self.task:
            self.task = asyncio.ensure_future(self.run())

    @abstractmethod
    async def run(self):
        ...

    def subscribe(self, fn):
        print('subscribed')
        self.listener = fn

    def unsubscribe(self):
        self.listener = None
