import io
import math
import sys
import ujson as json

from PIL import Image, ImageDraw
from websocket import create_connection

sys.path.append('../')

from config import SERVER
from slam import Slam


def map_listener(ws, pose_caller):
    def map_callback(map_data):
        print('map_datacalback')

        data = bytearray([x + 1 for x in map_data['data']])
        shape = (map_data['info']['width'], map_data['info']['height'])
        resolution = map_data['info']['resolution']
        x_origin = map_data['info']['origin']['position']['x']
        y_origin = map_data['info']['origin']['position']['y']
        img = Image.frombuffer('L', shape, data, 'raw', 'L', 0, 1)

        pose = pose_caller()
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

        ws.send(json.dumps({'action': 'map', 'data': bytearray(bytes_img.getvalue())}))

    return map_callback


if __name__ == '__main__':
    ws = create_connection(f"ws://{SERVER['HOST']}:{SERVER['PORT']}")
    try:
        slam = Slam()
        pose_caller = slam.pose_caller()

        slam.register_map_listener(map_listener(ws, pose_caller))
        while True:
            pass
    finally:
        ws.close()
