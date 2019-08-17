from dataclasses import dataclass


@dataclass
class SensorData:
    x: float
    y: float
    z: float

    def __repr__(self):
        return f'{self.x},{self.y},{self.z}'

    def __str__(self):
        return self.__repr__()


@dataclass
class IMUData:
    acc: SensorData
    gyro: SensorData
    mag: SensorData

    @staticmethod
    def header():
        return ",".join([f'{sens}_{ax}' for sens in ('acc', 'gyro', 'mag') for ax in ('x', 'y', 'z')])

    def __repr__(self):
        return f'{self.acc},{self.gyro},{self.mag}'

    def __str__(self):
        return self.__repr__()

    @classmethod
    def parse(cls, acc, gyro, mag):
        if isinstance(acc, dict):
            return cls(*[SensorData(s['x'], s['y'], s['z']) for s in (acc, gyro, mag)])
        elif isinstance(acc, (list, tuple)):
            return cls(*[SensorData(*s) for s in (acc, gyro, mag)])
        else:
            print("Unsupported sensor data datatype")
