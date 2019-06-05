import asyncio
import os
from contextlib import suppress

from breezyslam.algorithms import RMHC_SLAM
from breezyslam.sensors import RPLidarA1
from rplidar import RPLidar

from config import SLAM
from sensors.lidar.lidar_base import BaseLidar


def mm2pix(mm):
    return int(mm / (SLAM['MAP_SIZE_METERS'] * 1000. / SLAM['MAP_SIZE_PIXELS']))


class Lidar(BaseLidar):

    def __init__(self):
        super().__init__()
        self.lidar = RPLidar(os.getenv('LIDAR_DEVICE', SLAM["LIDAR_DEVICE"]))
        self.slam = RMHC_SLAM(RPLidarA1(), SLAM['MAP_SIZE_PIXELS'], SLAM['MAP_SIZE_METERS'])
        self.trajectory = []
        self.mapbytes = bytearray(SLAM['MAP_SIZE_PIXELS'] * SLAM['MAP_SIZE_PIXELS'])
        self.prev_checksum = 0

    async def stop(self):
        await super().stop()
        self.lidar.stop()
        self.lidar.stop_motor()
        self.lidar.disconnect()

    async def run(self):
        previous_distances = None
        previous_angles = None
        iterator = self.lidar.iter_scans()
        next(iterator)

        while True:
            items = [(q, 360 - angle, dist) for q, angle, dist in next(iterator)]
            distances = [item[2] for item in items]
            angles = [item[1] for item in items]

            if len(distances) > SLAM['MIN_SAMPLES']:
                self.slam.update(distances, scan_angles_degrees=angles)
                previous_distances = distances.copy()
                previous_angles = angles.copy()
            elif previous_distances is not None:
                self.slam.update(previous_distances, scan_angles_degrees=previous_angles)

            x, y, theta = self.slam.getpos()
            self.trajectory.append((x, y))

            self.slam.getmap(self.mapbytes)

            for coords in self.trajectory:
                x_mm, y_mm = coords

                x_pix = mm2pix(x_mm)
                y_pix = mm2pix(y_mm)

                self.mapbytes[y_pix * SLAM['MAP_SIZE_PIXELS'] + x_pix] = 0
            checksum = sum(self.mapbytes)
            print(self.listener)
            if self.listener and checksum != self.prev_checksum:
                print(checksum)
                await self.listener(self.mapbytes)

            self.prev_checksum = checksum
