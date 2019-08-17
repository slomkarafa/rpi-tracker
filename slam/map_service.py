import io
import math
import sys
import ujson as json

from PIL import Image, ImageDraw
from websocket import create_connection

sys.path.append('../')

from config import SERVER
from slam import Slam


def parse_map_and_pose(map_data, pose):

    data = bytearray([x + 1 for x in map_data['data']])
    shape = (map_data['info']['width'], map_data['info']['height'])
    resolution = map_data['info']['resolution']
    x_origin = map_data['info']['origin']['position']['x']
    y_origin = map_data['info']['origin']['position']['y']
    img = Image.frombuffer('L', shape, data, 'raw', 'L', 0, 1)

    angle = int(math.degrees(math.acos(pose.orient.w) * 2))
    position = pose.posit

    x = int((position.x-x_origin)/resolution)
    y = int((position.y-y_origin)/resolution)

    print(x)
    print(y)
    print(angle)
    print(shape)

    draw = ImageDraw.Draw(img)
    draw.pieslice([x-20, y-20, x+20, y+20], angle-20, angle+20, 'green', 'blue')

    bytes_img = io.BytesIO()
    img.save(bytes_img, format='PNG')

    return bytearray(bytes_img.getvalue())


class ResultWrapper:
    def __init__(self):
        self.result = None

    def reset(self):
        self.result = None

    def call(self, result):
        self.result = result


if __name__ == '__main__':
    ws = create_connection(f"ws://{SERVER['HOST']}:{SERVER['PORT']}/map")
    try:
        slam = Slam()
        pose_caller = slam.pose_caller()
        map_resp = ResultWrapper()
        slam.register_map_listener(map_resp.call)
        while True:
            if map_resp.result:
                pose = pose_caller()
                result = parse_map_and_pose(map_resp.result, pose)
                map_resp.reset()

                ws.send(json.dumps({'action': 'map', 'data': result}))

    finally:
        ws.close()
