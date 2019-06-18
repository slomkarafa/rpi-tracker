#!/usr/bin/env bash
#source activate rpi-tracker
source activate rplidar

trap 'kill %1' SIGINT

PYTHONPATH=$PYTHONPATH:../ python communication/service.py &
sleep 2
PYTHONPATH=$PYTHONPATH:../ python slam/service.py

