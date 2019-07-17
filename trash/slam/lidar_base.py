import asyncio
from abc import ABC, abstractmethod
from contextlib import suppress


class BaseLidar(ABC):

    def __init__(self, on_map_change=None):
        self.on_map_change = on_map_change

    @abstractmethod
    def run(self):
        ...
