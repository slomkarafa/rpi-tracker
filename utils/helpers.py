import os

from config import HARDWARE_ACTIVE


def should_use(device):
    return not os.getenv('UNPLUGGED', 'False').lower() == 'true' and HARDWARE_ACTIVE[device]
