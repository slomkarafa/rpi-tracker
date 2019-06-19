#!/usr/bin/env bash
#source activate rpi-tracker
#source activate rplidar

trap 'kill -9 $(lsof -t -i:8080)' EXIT


UNPLUGGED=False PYTHONPATH=$PYTHONPATH:/home/pi/Projects/rpi-tracker/:/home/pi/Projects/rpi-tracker/communication/ /home/pi/.virtualenvs/xxx/bin/python /home/pi/Projects/rpi-tracker/communication/service.py &
sleep 2
sudo PYTHONPATH=$PYTHONPATH:/home/pi/Projects/rpi-tracker/:/home/pi/Projects/rpi-tracker/slam/ /home/pi/.virtualenvs/xxx/bin/python /home/pi/Projects/rpi-tracker/slam/run.py &

