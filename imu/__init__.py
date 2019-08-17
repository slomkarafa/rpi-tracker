import sys

sys.path.append('../')

from utils.helpers import should_use

if should_use('GPIO'):
    from imu.mpu_9250 import MPU9250 as IMU
else:

    from imu.fake_imu import FakeIMU as IMU
