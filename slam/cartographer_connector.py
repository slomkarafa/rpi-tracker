import os

import roslibpy
import time
# import ujson as json
import json

from config import CARTOGRAPHER_ROS
from slam.slam_interface import Slam


class CartographerConnector(Slam):

    def __init__(self):
        self.cli = roslibpy.Ros(host=os.getenv('CARTOGRAPHER_HOST', CARTOGRAPHER_ROS['HOST']),
                                port=os.getenv('CARTOGRAPHER_PORT', CARTOGRAPHER_ROS['PORT']))
        self.map_listener = None
        self.submap_list_listener = None
        self.submap_query_service = None
        self.trajectory_query_service = None
        self.time_service = None
        self.trajectory_result = PoseCaller()
        self.cli.run()

    def register_map_listener(self, callback):
        self.map_listener = roslibpy.Topic(self.cli, '/map', 'nav_msgs/OccupancyGrid')

        def wrapped_callback(msg):
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
            print(raw_callback)
            msg = raw_callback.get('trajectory', [None])[-1]
            callback(msg)

        return handle_raw

    def register_trajectory_service(self, main_callback=None):
        self.trajectory_query_service = roslibpy.Service(self.cli, '/trajectory_query',
                                                         '/cartographer_ros_msgs/TrajectoryQuery')

        def call_trajectory(exact_callback=None, msg=None):
            callback = exact_callback if exact_callback else main_callback
            request = roslibpy.ServiceRequest({"trajectory_id": 0})
            # self.trajectory_query_service.call(request, self._handle_trajectory(callback), self.error)
            if msg:
                print(f'before {msg}')
            self.trajectory_query_service.call(request, callback, self.error)
            if msg:
                print(f'after {msg}')

        return call_trajectory

    def __del__(self):
        self.cli.terminate()

    def register_time_service(self, main_callback=None):
        self.time_service = roslibpy.Service(self.cli, '/read_metrics', '/cartographer_ros_msgs/ReadMetrics')

        def call_time(exact_callback=None):
            callback = exact_callback if exact_callback else main_callback

            def time_wrapper(msg):
                resp = msg['timestamp']
                callback(resp)

            request = roslibpy.ServiceRequest(dict())
            self.time_service.call(request, time_wrapper, self.error)

        return call_time


def call(msg):
    pass
    # print(msg)


class TimeCaller:
    def __init__(self):
        self.chkpt = time.time()

    def call(self, callback, count):
        def wrapped(msg):
            then = self.chkpt
            self.chkpt = time.time()
            callback(msg)
            print(f'Between maps: {self.chkpt - then}')
            print(f'after{count} {self.chkpt}')

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


class SaveCaller2:
    def __init__(self, base_name):
        self.base_name = base_name
        self.file = open(base_name, 'w')
        self.file.write('ts,data\n')

    def call(self, callback):
        def wrapped(msg):
            callback(msg)
            self.file.write(f'{time.time()};{json.dumps(dict(msg))}\n')

        return wrapped

    def __del__(self):
        self.file.close()


class PoseCaller:
    def __init__(self):
        self.pose = None

    def call(self, resp):
        print('parsingpose')
        # self.pose = PoseData.parse(resp['pose'])
        self.pose = True

    def reset(self):
        self.pose = None


def test_0(x, save, timer):
    service = x.register_trajectory_service()

    print(f'1 {time.time()}')
    service(save.call(timer.call(call, 1)), msg=1)
    time.sleep(1)
    print(f'2 {time.time()}')
    service(save.call(timer.call(call, 2)), msg=2)
    print(f'3 {time.time()}')
    service(save.call(timer.call(call, 3)), msg=3)
    # x.register_map_listener(caller)
    # x.register_map_listener(call)
    # x.register_trajectory_service(caller.call(lambda _: None))()

def test_time(x):
    serv = x.register_time_service(call)
    serv()

def analyze():
    with open('data/test0.csv') as f:
        header = f.readline()
        res = []
        for _ in (1, 2, 3):
            row = f.readline().split(';')
            res.append(json.loads(row[1]))
        for x in res:
            y = x['trajectory'][-3:]
            for z in y:
                print(z)
            print()


if __name__ == '__main__':
    save = SaveCaller2('data/test0.csv')
    timer = TimeCaller()
    x = CartographerConnector()

    test_0(x, save, timer)
    # test_time(x)
    print('tu jestem')
    try:
        while True:
            pass
    except KeyboardInterrupt:
        del save
        analyze()
