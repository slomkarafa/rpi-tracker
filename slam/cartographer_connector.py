import os

import roslibpy
import time
# import ujson as json
import json

from config import CARTOGRAPHER_ROS
from slam_interface import Slam


class CartographerConnector(Slam):
    def __init__(self):
        self.cli = roslibpy.Ros(host=os.getenv('CARTOGRAPHER_HOST', CARTOGRAPHER_ROS['HOST']),
                                port=os.getenv('CARTOGRAPHER_PORT', CARTOGRAPHER_ROS['PORT']))
        self.map_listener = None
        self.submap_list_listener = None
        self.submap_query_service = None
        self.trajectory_query_service = None
        self.cli.run()

    def register_map_listener(self, callback):
        self.map_listener = roslibpy.Topic(self.cli, '/map', 'nav_msgs/OccupancyGrid')

        def wrapped_callback(msg):
            if self.save:
                with open(f'data/map_{self.b}.json', 'x') as file:
                    file.write(json.dumps(msg))
            self.b += 1
            callback(msg)

        self.map_listener.subscribe(wrapped_callback)

    @staticmethod
    def error(msg):
        print('Error:')
        print(msg)

    def _handle_submap_list(self, callback):
        self.chkpt = time.time()

        def handler(msg):
            print(msg)
            submap = msg['submap'][-1]

            def query_callback(msg1):
                print(msg1)
                # print(msg['textures'][-1]['slice_pose'])
                then = self.chkpt
                self.chkpt = time.time()
                print(f'Between maps: {self.chkpt - then}')
                if self.save:
                    with open(f'data/submaps_{self.a}.json', 'x') as file:
                        file.write(json.dumps({'all': dict(msg), 'last': dict(msg1)}))
                self.a += 1
                callback({'all': msg, 'last': msg1})

            # print(submap['pose'])

            request = roslibpy.ServiceRequest({"trajectory_id": 0, "submap_index": submap["submap_index"]})
            self.submap_query_service.call(request, query_callback, self.error)

        return handler

    def register_submap_listener(self, callback):
        self.submap_list_listener = roslibpy.Topic(self.cli, '/submap_list', 'cartographer_ros_msgs/SubmapList')
        self.submap_query_service = roslibpy.Service(self.cli, '/submap_query', '/cartographer_ros_msgs/SubmapQuery')
        self.submap_list_listener.subscribe(self._handle_submap_list(callback))

    def _handle_trajectory(self, callback):
        def handle_raw(raw_callback):
            msg = raw_callback.get('trajectory', [None])[-1]
            if self.save:
                with open(f'data/trajectory_{self.a}.json', 'x') as file:
                    file.write(json.dumps(msg))
            callback(msg)

        return handle_raw

    def register_trajectory_service(self, callback):
        self.trajectory_query_service = roslibpy.Service(self.cli, '/trajectory_query',
                                                         '/cartographer_ros_msgs/TrajectoryQuery')

        def call_trajectory():
            request = roslibpy.ServiceRequest({"trajectory_id": 0})
            self.trajectory_query_service.call(request, self._handle_trajectory(callback), self.error)

        return call_trajectory

    def __del__(self):
        self.cli.terminate()


def call(msg):
    # pass
    print(msg)


class TimeCaller:
    def __init__(self):
        self.chkpt = time.time()

    def call(self, callback):
        def wrapped(msg):
            then = self.chkpt
            self.chkpt = time.time()
            callback(msg)
            print(f'Between maps: {self.chkpt - then}')

        return wrapped


class SaveCaller:
    def __init__(self, base_name):
        self.base_name = base_name
        self.counter = 0

    def call(self, callback):
        def wrapped(msg):
            callback(msg)
            with open(f'data/{self.base_name}_{self.counter}.json', 'x') as file:
                file.write(json.dumps(msg))
            self.counter += 1

        return wrapped


if __name__ == '__main__':
    x = CartographerConnector()

    # x.register_for_submap(call)
    # x.register_map_listener(call)
    x.register_trajectory_service(call)()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        del x