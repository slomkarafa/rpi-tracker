import os
import sys

from config import UNPLUGGED

sys.path.append('../')

if os.getenv('UNPLUGGED', UNPLUGGED) == 'True':
    from slam.lidar_mock import MockLidar as Lidar
else:
    from slam.lidar import Lidar
