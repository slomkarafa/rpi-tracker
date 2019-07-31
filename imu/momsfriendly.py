# !/usr/bin/env python

import mpu9250
import time
from time import sleep

imu = mpu9250.mpu9250.mpu9250()

try:
    while True:
        chkpt = time.time()

        a = imu.accel
        g = imu.gyro
        m = imu.mag
        print(f'measurement time: {time.time()-chkpt}')

        print('Accel: {:.3f} {:.3f} {:.3f} mg'.format(*a))
        print('Gyro: {:.3f} {:.3f} {:.3f} dps'.format(*g))
        print('Magnet: {:.3f} {:.3f} {:.3f} mT'.format(*m))
        m = imu.temp
        print('Temperature: {:.3f} C'.format(m))
        print()
        sleep(0.2)
except KeyboardInterrupt:
    print('bye ...')
