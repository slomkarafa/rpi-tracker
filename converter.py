import math
import numpy as np


def circle_to_drives(angle, power):
    ratio = math.cos(math.radians(angle))
    sin = math.sin(math.radians(angle))

    multiplier = power * (-1 if sin < 0 else 1)

    drives = np.array([1 - ratio, 1] if ratio > 0 else [1, 1 + ratio]) * multiplier
    # drives = np.array(
    #     [1 - ratio, ratio] if abs(sin) < 0.1 else [1 - ratio, 1 - ratio]) * multiplier

    return drives
