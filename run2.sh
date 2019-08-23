source ros2/devel_isolated/setup.bash

ROS_MASTER_URI=http://localhost:11311

fuser -k 8080/tcp

#roslaunch ros/slam.launch
PYTHON=/home/pi/.virtualenvs/tracker2/bin/python
PYTHONPATH=$PYTHONPATH:./ ${PYTHON} communication/service.py & PYTHONPATH=$PYTHONPATH:./ ${PYTHON} data_aquisition/collector.py & PYTHONPATH=$PYTHONPATH:./
