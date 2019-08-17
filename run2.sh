source ros2/devel_isolated/setup.bash
cd ros3 && roslaunch slam.launch

workon tracker2

fuser -k 8080/tcp

PYTHONPATH=$PYTHONPATH:./ python communication/service.py & PYTHONPATH=$PYTHONPATH:./ python data_aquisition/collector.py & PYTHONPATH=$PYTHONPATH:./ python slam/map_service.py
