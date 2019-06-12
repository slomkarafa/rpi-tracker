import os

from config import UNPLUGGED

if os.getenv('UNPLUGGED', UNPLUGGED) == 'True':
    from sensors.lidar.lidar_mock import MockLidar as Lidar
else:
    from sensors.lidar.lidar import Lidar
