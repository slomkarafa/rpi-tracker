from dataclasses import dataclass


@dataclass
class PositionData:
    x: float
    y: float
    z: float

    def __repr__(self):
        return f'{self.x},{self.y}, {self.z}'


@dataclass
class OrientationData:
    x: float
    y: float
    z: float
    w: float

    def __repr__(self):
        return f'{self.x},{self.y},{self.z},{self.w}'


@dataclass
class PoseData:
    posit: PositionData
    orient: OrientationData

    def __repr__(self):
        return f'{self.posit},{self.orient}'

    @classmethod
    def parse(cls, pose):
        posit, orient = pose['position'], pose['orientation']
        return cls(PositionData(posit['x'], posit['y'], posit['z']),
                   OrientationData(orient['x'], orient['y'], orient['z'], orient['w']))
