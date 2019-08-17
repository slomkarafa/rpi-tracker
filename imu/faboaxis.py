import FaBo9Axis_MPU9250

import time

import sys

mpu9250 = FaBo9Axis_MPU9250.MPU9250()

try:

    while True:
        chkpt = time.time()
        accel = mpu9250.readAccel()
        gyro = mpu9250.readGyro()
        mag = mpu9250.readMagnet()
        print(f'measurement time: {time.time()-chkpt}')

        print(f"ax = {accel['x']}")

        print(f"ay = {accel['y']}")

        print(f"az = {accel['z']}")


        print(f"gx = {gyro['x']}")

        print(f"gy = {gyro['y']}")

        print(f"gz = {gyro['z']}")


        print(f"mx = {mag['x']}")

        print(f"my = {mag['y']}")

        print(f"mz = {mag['z']}")

        print()

        time.sleep(0.2)

except KeyboardInterrupt:

    sys.exit()
