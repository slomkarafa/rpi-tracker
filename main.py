# import RPi.GPIO as GPIO
import time
from motor import Motor
from server import start
from steering import Rider
import argparse
import json
import asyncio

parser = argparse.ArgumentParser(description='Rpi-tracker main app')
parser.add_argument('-c', '--config', default='config.json', help='Path to config file')


async def tester(rider):
    for x in range(0, 100, 10):
        rider.ride(x, x)
        time.sleep(5)
    rider.stop()


def main(config):
    # r = config['MOTORS']['RIGHT']
    # l = config['MOTORS']['LEFT']
    #
    # right_motor = Motor(r['pwm'], r['dir_0'], r['dir_1'])
    # left_motor = Motor(l['pwm'], l['dir_0'], l['dir_1'])
    #
    # rider = Rider(left_motor, right_motor)

    start(config)
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(tester(rider))
    # loop.close()
    # tester(rider)
    # rider.stop()


if __name__ == '__main__':
    args = parser.parse_args()
    with open(args.config, 'r') as f:
        config = json.loads(f.read())
    print(json)
    try:
        main(config)
    finally:
        # GPIO.cleanup()
        pass
