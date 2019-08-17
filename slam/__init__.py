from utils.helpers import should_use

if should_use('LIDAR'):
    from slam.cartographer_connector import CartographerConnector as Slam
else:
    from slam.mock import SlamMock as Slam
