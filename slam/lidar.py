import os
import io

import numpy as np
from PIL import Image

from breezyslam.algorithms import RMHC_SLAM
from breezyslam.sensors import RPLidarA1
from roboviz import MapVisualizer
from rplidar import RPLidar

from config import SLAM
from slam.lidar_base import BaseLidar


def mm2pix(mm):
    return int(mm / (SLAM['MAP_SIZE_METERS'] * 1000. / SLAM['MAP_SIZE_PIXELS']))


class Lidar(BaseLidar):

    def __init__(self, on_map_change):
        super().__init__(on_map_change=on_map_change)
        self.lidar = RPLidar(os.getenv('LIDAR_DEVICE', SLAM["LIDAR_DEVICE"]))
        self.slam = RMHC_SLAM(RPLidarA1(), SLAM['MAP_SIZE_PIXELS'], SLAM['MAP_SIZE_METERS'])
        self.map_size_pixels = SLAM['MAP_SIZE_PIXELS']
        self.trajectory = []
        self.mapbytes = bytearray(SLAM['MAP_SIZE_PIXELS'] * SLAM['MAP_SIZE_PIXELS'])
        self.prev_checksum = 0
        self.viz = MapVisualizer(SLAM['MAP_SIZE_PIXELS'], SLAM['MAP_SIZE_METERS'], 'SLAM')

    def stop(self):
        # await super().stop()
        self.lidar.stop()
        self.lidar.stop_motor()
        self.lidar.disconnect()

    def run(self):
        try:
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
                if self.on_map_change and checksum != self.prev_checksum:
                    # print(checksum)
                    x = Image.frombuffer('L', (self.map_size_pixels, self.map_size_pixels), self.mapbytes, 'raw', 'L', 0, 1)
                    bytes_img = io.BytesIO()
                    x.save(bytes_img, format='PNG')
                    self.on_map_change(bytearray(bytes_img.getvalue()))
                self.prev_checksum = checksum
        except Exception as e:
            print(e)
        finally:
            self.stop()
