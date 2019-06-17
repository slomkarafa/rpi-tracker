import os

from config import UNPLUGGED

if os.getenv('UNPLUGGED', UNPLUGGED) == 'True':
    pass
else:
    pass
