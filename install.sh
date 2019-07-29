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

mkdir -p ros/ && cd ros/



## option 2 - optimised(not complited yet)
sudo apt-get install -y python-rosdep python-rosinstall-generator python-wstool python-rosinstall build-essential cmake ninja-build


sudo rosdep init
rosdep update
#rosinstall_generator ros_comm sensor_msgs pcl_msgs eigen_conversions visualization_msgs trajectory_msgs urdf --rosdistro melodic --deps --wet-only --tar > melodic-ros_comm-wet.rosinstall

rosinstall_generator ros_comm sensor_msgs pcl_msgs eigen_conversions visualization_msgs --rosdistro melodic --deps --wet-only --tar > melodic-ros_comm-wet.rosinstall
wstool init src melodic-ros_comm-wet.rosinstall

#! on rpi add line to catographer CMakes.txt: set(CMAKE_CXX_LINK_FLAGS "${CMAKE_CXX_LINK_FLAGS} -latomic")
wstool merge -t src https://raw.githubusercontent.com/googlecartographer/cartographer_ros/master/cartographer_ros.rosinstall
wstool update -t src

git clone https://github.com/RobotWebTools/rosbridge_suite.git
git clone https://github.com/robopeak/rplidar_ros.git

cd src/cartographer && git checkout master && cd ../..
cd src/cartographer_ros && git checkout master && cd ../..

src/cartographer/scripts/install_proto3.sh

rosdep update
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



catkin_make_isolated --install --use-ninja --source external_src
Base path: /home/pi/rpi-tracker/ros
Source space: /home/pi/rpi-tracker/ros/src


rosbridge_library: No definition of [trajectory_msgs] for OS version [buster]
cartographer_ros: No definition of [urdf] for OS version [buster]
cartographer_rviz: No definition of [rviz] for OS version [buster]
rosbridge_server: No definition of [rosauth] for OS version [buster]
Continuing to install resolvable dependencies...