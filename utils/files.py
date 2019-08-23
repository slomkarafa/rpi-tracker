import ujson as json


def load_json(path):
    with open(path, 'r') as file:
        return json.load(file)


def save_json(dictable, path):
    with open(path, 'w') as file:
        json.dump(dict(dictable), file)
