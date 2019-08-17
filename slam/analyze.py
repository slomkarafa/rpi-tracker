import numpy as np
import matplotlib.pyplot as plt

from utils.files import load_json

map = load_json('data/map_15.json')

submaps = load_json('data/submaps_52.json')
all_subs = submaps['all']
last_subs = submaps['last']

data = map['data']
dims = [-130,189]
print(bytes([x+1 for x in data]))
_data = np.array(data).reshape(dims)
plt.imshow(_data)
plt.show()