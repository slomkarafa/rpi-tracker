import RPi.GPIO as GPIO
import time
from motor import Motor
from server import init
from steering import Rider
import argparse
import json

parser = argparse.ArgumentParser(description='Rpi-tracker main app')
parser.add_argument('-c', '--config', default='config.json', help='Path to config file')


# try:
#     x = 1
#     motor = Motor(17, 27, 22)
#     motor.set_direction('FORWARD')
#     while 1:
#
#         for x in range(100):
#             motor.set_speed(x)
#             time.sleep(0.1)
#
#         for x in range(100):
#             motor.set_speed(100 - x)
#             time.sleep(0.1)
#
#         motor.change_direction()
# finally:
#     GPIO.cleanup()


def main(config):
    r = config['MOTORS']['RIGHT']
    l = config['MOTORS']['LEFT']

    right_motor = Motor(r['pwm'], r['dir_0'], r['dir_1'])
    left_motor = Motor(l['pwm'], l['dir_0'], l['dir_1'])

    rider = Rider(left_motor, right_motor)

    init(config['SERVER'], rider)
    rider.stop()


if __name__ == '__main__':
    args = parser.parse_args()
    with open(args.config, 'r') as f:
        config = json.loads(f.read())
    print(json)
    try:
        main(config)
    finally:
        GPIO.cleanup()
