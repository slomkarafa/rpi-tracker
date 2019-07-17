import ujson as json


def load_json(path):
    with open(path, 'r') as file:
        return json.load(file)