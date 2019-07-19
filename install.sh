sudo apt-get install build-essential checkinstall python-pip python3-pip -y

sudo pip2 install virtualenv virtualenvwrapper
sudo pip3 install virtualenv virtualenvwrapper
echo "# Virtual Environment Wrapper"  >> ~/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
source ~/.bashrc

mkvirtualenv tracker -p python3

# ROS
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo -E apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

sudo apt-get update
sudo apt-get upgrade

sudo apt-get install -y python-rosdep python-rosinstall-generator python-wstool python-rosinstall build-essential cmake ninja-build


mkdir -p ros/ && cd ros/
sudo rosdep init
rosdep update
rosinstall_generator ros_comm sensor_msgs --rosdistro melodic --deps --wet-only --tar > melodic-ros_comm-wet.rosinstall
wstool init src melodic-ros_comm-wet.rosinstall
rosdep install -y --from-paths src --ignore-src --rosdistro melodic -r --os=debian:buster

sudo ./src/catkin/bin/catkin_make_isolated --install -DCMAKE_BUILD_TYPE=Release --install-space /opt/ros/melodic

echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc

source ~/.bashrc
workon tracker
pip install tornado==4.5.3
mv src ros_src
mkdir src
cd src
catkin_init_workspace

git clone https://github.com/RobotWebTools/rosbridge_suite.git
git clone https://github.com/robopeak/rplidar_ros.git
git clone https://github.com/googlecartographer/cartographer_ros.git

catkin_make_isolated --install --use-ninja --source external_src
Base path: /home/pi/rpi-tracker/ros
Source space: /home/pi/rpi-tracker/ros/src
