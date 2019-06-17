import sys

import rpyc

sys.path.append('../')

from config import DISTRIBUTED
from slam import Lidar



def register_callback(conn):
    def handle(msg):
        rpyc.async_(conn.update_map(msg))

    return handle


if __name__ == "__main__":
    c = rpyc.connect("localhost", DISTRIBUTED['REST'])

    slam = Lidar(register_callback(c))
    slam.start()
