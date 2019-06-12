import os

from config import UNPLUGGED

if os.getenv('UNPLUGGED', UNPLUGGED) == 'True':
    from steering.rider.rider_unplugged import UnpluggedRider as Rider
else:
    from steering.rider.rider import Rider
