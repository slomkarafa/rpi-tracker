SERVER = {
    "port": 8080
}
STEERING = {
    "FW": "FORWARD",
    "RV": "REVERSE",
    "LF": "LEFT",
    "RH": "RIGHT",
    "ST": "START",
    "SP": "STOP",
    "UP": "SPEEDUP",
    "DN": "SPEEDDOWN"
}
MOTORS = {
    "LEFT": {
        "pwm": 18,
        "dir_0": 23,
        "dir_1": 24
    },
    "RIGHT": {
        "pwm": 12,
        "dir_0": 25,
        "dir_1": 17
    }
}

PIGPIO = {
    'HOST': 'localhost',
    "PORT": 8888
}

SLAM = {
    "MAP_SIZE_PIXELS": 500,
    "MAP_SIZE_METERS": 10,
    "LIDAR_DEVICE": '/dev/ttyUSB0',
    # "MIN_SAMPLES": 200
    "MIN_SAMPLES": 100
}

UNPLUGGED = 'True'

DISTRIBUTED = {
    'SLAM': 50045,
    'REST': 50046
}