from dataclasses import dataclass


@dataclass
class PositionData:
    x: float
    y: float
    z: float

    def __repr__(self):
        return f'{self.x},{self.y},{self.z}'

    def __str__(self):
        return self.__repr__()


@dataclass
class OrientationData:
    x: float
    y: float
    z: float
    w: float

    def __repr__(self):
        return f'{self.x},{self.y},{self.z},{self.w}'

    def __str__(self):
        return self.__repr__()


@dataclass
class PoseData:
    posit: PositionData
    orient: OrientationData

    @staticmethod
    def header():
        return ",".join([*[f'{sens}_{ax}' for sens in ('posit', 'orient') for ax in ('x', 'y', 'z')], 'orient_w'])

    def __repr__(self):
        return f'{self.posit},{self.orient}'

    def __str__(self):
        return self.__repr__()

    @classmethod
    def parse(cls, pose):
        posit, orient = pose['position'], pose['orientation']
        return cls(PositionData(posit['x'], posit['y'], posit['z']),
                   OrientationData(orient['x'], orient['y'], orient['z'], orient['w']))
