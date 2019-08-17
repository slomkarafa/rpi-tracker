from abc import ABC, abstractmethod


class IMU(ABC):
    @abstractmethod
    def get_measurements(self):
        ...
