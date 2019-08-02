import FaBo9Axis_MPU9250

from imu.imu import IMU
from imu.imu_model import IMUData


class MPU9250(IMU):
    def __init__(self):
        self.mpu = FaBo9Axis_MPU9250.MPU9250()

    def get_measurements(self):
        acc = self.mpu.readAccel()
        gyro = self.mpu.readGyro()
        mag = self.mpu.readMagnet()
        return IMUData.parse(acc, gyro, mag)
