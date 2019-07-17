from abc import ABC, abstractmethod


class Slam(ABC):

    @abstractmethod
    def register_map_listener(self, callback):
        ...

    @abstractmethod
    def register_submap_listener(self, callback):
        ...

    @abstractmethod
    def register_trajectory_service(self, callback):
        ...
