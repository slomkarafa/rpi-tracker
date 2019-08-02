from imu.imu import IMU
from imu.imu_model import IMUData


class FakeIMU(IMU):
    def get_measurements(self):
        return IMUData.parse([0, 0, 0], [0, 0, 0], [0, 0, 0])
