# Testing - unplugged env

## installation
 - python3.7 is required
 - then: `pip install -r requirements.txt`
 
 ## run
 `python main.py`




#RPI

sudo apt-get install build-essential checkinstall
sudo apt-get install libreadline-gplv2-dev  libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

sudo wget https://www.python.org/ftp/python/3.6.6/Python-3.6.6.tgz
tar xzvf Python-3.6.6.tgz
cd Python-3.6.6/
./configure  --enable-optimizations
sudo make -j4
sudo make install
cd .. && sudo rm -rf Python-3* 

# create a virtual environment for python 3
mkvirtualenv virtual-py3 -p python3.6
# Activate the virtual environment
workon virtual-py3

## install RPi.GPIO library
wget https://pypi.python.org/packages/source/R/RPi.GPIO/RPi.GPIO-0.6.4.tar.gz
tar -xvf RPi.GPIO-0.6.4.tar.gz
cd RPi.GPIO-0.6.4/
python setup.py install
cd .. && rm -rf RPi.GPIO-0.*
