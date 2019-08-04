from abc import ABC, abstractmethod

from slam.pose_model import PoseData


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

    def pose_caller(self):
        result = PoseCaller()

        service = self.register_trajectory_service(result.call)

        def caller():
            result.reset()
            service()

            while not result.pose:
                pass
            return result.pose

        return caller


class PoseCaller:
    def __init__(self):
        self.pose = None

    def call(self, resp):
        self.pose = PoseData.parse(resp['pose'])

    def reset(self):
        self.pose = None
