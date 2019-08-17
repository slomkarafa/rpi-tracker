import os

from slam.slam_interface import Slam
from utils.files import load_json


class SlamMock(Slam):
    def __init__(self, *_, **__):
        self.map = None
        self.submap = None
        self.trajectory = None

    def register_map_listener(self, callback):
        self.map = load_json(f'{os.path.dirname(os.path.realpath(__file__))}/data/map_15.json')
        callback(self.map)

    def register_submap_listener(self, callback):
        self.submap = load_json(f'{os.path.dirname(os.path.realpath(__file__))}/data/submaps_50.json')
        callback(self.submap)

    def register_trajectory_service(self, callback):
        self.trajectory = load_json(f'{os.path.dirname(os.path.realpath(__file__))}/data/trajectory_0.json')

        def call():
            callback(self.trajectory)

        return call
