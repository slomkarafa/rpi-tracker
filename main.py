# import RPi.GPIO as GPIO
from communication.server import run
import argparse


parser = argparse.ArgumentParser(description='Rpi-tracker main app')
parser.add_argument('-c', '--config.py', default='config.py', help='Path to config.py file')


def main():
    run()


if __name__ == '__main__':

    try:
        main()
    finally:
        # GPIO.cleanup()
        pass
