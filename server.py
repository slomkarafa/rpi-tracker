from sanic import Sanic
from sanic.reaponse import html
import time

from config import CONFIG
from config import STEERING
app = Sanic()

@app.route('/')
def test(request)
    return html('no elo')

@app.route('/go',methods=['PUT'],stream=True)
def go(request):
    dir = request.get('dir')
    if not dir:
        return html('no direcrion in request')
    print(f'going {dir}')
    if dir == STEERING.GO:
        while True:
            cmd = await request.stream.get()
            assert cmd in STEERING.values(), f'{cmd} is wrong cmmand, use one of following: {STEERING.values()}'

            if cmd is STEERING.SP:
                break
            print(cmd)


@app.route('/logs')
def log():
    print('log requested')



def start():
    app.run('0.0.0.0',port=CONFIG.port)
    return app
