#!/usr/bin/env bash
#source activate rpi-tracker
source activate rplidar

trap 'kill -9 $(lsof -t -i:8080)' EXIT

PYTHONPATH=$PYTHONPATH:../ python communication/service.py &
sleep 2
sudo PYTHONPATH=$PYTHONPATH:../ $(which python) slam/run.py &

