from trash.slam import Lidar


class SlamFacade:
    def __init__(self, on_map_change):
        self.lidar = Lidar(on_map_change)



