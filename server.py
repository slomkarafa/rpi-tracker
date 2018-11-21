from sanic import Sanic
from sanic.reaponse import html
import time


# app = Sanic()
#
# @app.route('/')
# def test(request)
#     return html('no elo')
#
# @app.route('/go',methods=['PUT'],stream=True)
# def go(request):
#     dir = request.get('dir')
#     if not dir:
#         return html('no direcrion in request')
#     print(f'going {dir}')
#     if dir == STEERING.GO:
#         while True:
#             cmd = await request.stream.get()
#             assert cmd in STEERING.values(), f'{cmd} is wrong cmmand, use one of following: {STEERING.values()}'
#
#             if cmd is STEERING.SP:
#                 break
#             print(cmd)
#
#
# @app.route('/logs')
# def log():
#     print('log requested')

def get_start_func(rider):
    async def start(request):
        print('riding')
        rider.ride(100, 100)

    return start


def get_stop_func(rider):
    async def stop(request):
        print('stop')
        rider.stop()

    return stop


def init(config, rider):
    app = Sanic()
    app.add_route(get_start_func(rider), '/start', methods=['PUT'])
    app.add_route(get_stop_func(rider), '/stop', methods=['PUT'])

    app.run('0.0.0.0', port=config.SERVER.port)
    return app
