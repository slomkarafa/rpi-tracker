import sys

from service.ws_client import WebsocketService

sys.path.append('../')

# from lidar_mock import MockLidar as Lidar
from lidar import Lidar


if __name__ == "__main__":

    connection = WebsocketService()
    slam = Lidar(on_map_change=connection.send)
    slam.run()
