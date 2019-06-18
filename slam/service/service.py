from abc import ABC, abstractmethod


class ServiceI(ABC):

    @abstractmethod
    def send(self, msg):
        ...

    @abstractmethod
    def recv(self, msg):
        ...
