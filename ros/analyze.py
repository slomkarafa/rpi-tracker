import ujson as json


def load_josn(path):
    with open(path, 'r') as file:
        return json.load(file)


map = load_josn('data/map_16.json')

submaps = load_josn('data/submaps_52.json')
all_subs = submaps['all']
last_subs = submaps['last']