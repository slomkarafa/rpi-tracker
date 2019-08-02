from dataclasses import dataclass


@dataclass
class SensorData:
    x: float
    y: float
    z: float

    def __repr__(self):
        return f'{self.x},{self.y}, {self.z}'


@dataclass
class IMUData:
    acc: SensorData
    gyro: SensorData
    mag: SensorData

    def __repr__(self):
        return f'{self.acc},{self.gyro},{self.mag}'

    @classmethod
    def parse(cls, acc, gyro, mag):
        if isinstance(acc, dict):
            return cls(*[SensorData(s['x'], s['y'], s['z']) for s in (acc, gyro, mag)])
        elif isinstance(acc, (list, tuple)):
            return cls(*[SensorData(*s) for s in (acc, gyro, mag)])
        else:
            print("Unsupported sensor data datatype")
