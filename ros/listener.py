import roslibpy
import time
# import ujson as json
import json


class CartographerConnector:
    def __init__(self, host='localhost', port=9090, save=False):
        self.cli = roslibpy.Ros(host=host, port=port)
        self.save = save
        self.map_listener = None
        self.submap_list_listener = None
        self.submap_query_service = None
        self.trajectory_query_service = None
        self.chkpt = time.time()
        self.cli.run()
        self.a = 0
        self.b = 0
        self.c = 0

    def register_for_map(self, callback):
        self.map_listener = roslibpy.Topic(self.cli, '/map', 'nav_msgs/OccupancyGrid')

        def wrapped_callback(msg):
            then = self.chkpt
            self.chkpt = time.time()
            print(f'Between maps: {self.chkpt - then}')
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

    def handle_submap_list(self, callback):
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

    def register_for_submap(self, callback):
        self.submap_list_listener = roslibpy.Topic(self.cli, '/submap_list', 'cartographer_ros_msgs/SubmapList')
        self.submap_query_service = roslibpy.Service(self.cli, '/submap_query', '/cartographer_ros_msgs/SubmapQuery')
        self.submap_list_listener.subscribe(self.handle_submap_list(callback))

    @staticmethod
    def handle_trajectory(callback):
        def handle_raw(raw_callback):
            callback(raw_callback.get('trajectory', [None])[-1])

        return handle_raw

    def register_trajectory_service(self, callback):
        self.trajectory_query_service = roslibpy.Service(self.cli, '/trajectory_query',
                                                         '/cartographer_ros_msgs/TrajectoryQuery')

        def call_trajectory():
            request = roslibpy.ServiceRequest({"trajectory_id": 0})
            self.submap_query_service.call(request, self.handle_trajectory(callback), self.error)

        return call_trajectory

    def __del__(self):
        self.cli.terminate()


x = CartographerConnector()


def call(msg):
    # pass
    print(msg)


if __name__=='__main__':
    # x.register_for_submap(call)
    x.register_for_map(call)
    # x.register_for_trajectory(call)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        del x
