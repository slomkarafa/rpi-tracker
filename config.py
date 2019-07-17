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

HARDWARE_ACTIVE = {
    'LIDAR': True,
    'GPIO': False
}

CARTOGRAPHER_ROS = {
    'HOST': 'localhost',
    'PORT': 9090
}

DISTRIBUTED = {
    'SLAM': 50045,
    'REST': 50046
}