#!/usr/bin/env bash
source activate rpi-tracker

PYTHONPATH=$PYTHONPATH:../ python communication/service.py &
sleep 2
PYTHONPATH=$PYTHONPATH:../ python slam/service.py

