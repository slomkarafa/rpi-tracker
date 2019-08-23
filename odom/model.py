from dataclasses import dataclass


@dataclass
class OdometerData:
    left: int
    right: int

    @staticmethod
    def header():
        return "enc_left;enc_right"

    def __repr__(self):
        return f'{self.left};{self.right}'

    def __str__(self):
        return self.__repr__()
