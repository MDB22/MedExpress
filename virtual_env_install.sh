#!/bin/bash
LOG="virtual_env_install.log"
exec &> >(tee $LOG)

PYTHON="python_env"

echo "** Adding core programs **"
sudo apt-get install python3-venv python-pip

echo "** Building / Rebuilding python virtual env **"
rm -rf $PYTHON

echo "** Create virtual env **"
pyvenv $PYTHON
source $PYTHON/bin/activate

echo "** Upgrade pip in the virtual env"
pip install --upgrade pip

echo "** opencv"
sudo apt-get install build-essential
sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev

# build in home dir
cd ..

wget https://github.com/Itseez/opencv/archive/3.0.0.zip
unzip 3.0.0.zip

cd opencv-3.0.0
mkdir release
cd release

cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX="~/med_express_uav/opencv" -D PYTHON_EXECUTABLE=$(which python) ..

make -j 4
make install
cd med_express_uav

# link the python module as it doesn't install as part of the build
ln -s opencv/lib/python3.4/site-packages/cv2.cpython-34m.so $PYTHON/lib/python3.4/site-packages/cv2.cpython-34m.so

echo "** Dronekit: Setup dependecies **"
sudo apt-get build-dep python3-numpy python-opencv python3-serial python3-pyparsing
sudo apt-get install dpkg-dev build-essential python3-dev libjpeg-dev libtiff-dev libsdl1.2-dev libgstreamer-plugins-base0.10-dev 
echo "** Dronekit: Install python modules **"
pip install numpy pyparsing pyserial

# Hopefully can get away with not installing this will take a long time to build
#pip install -U --pre -f http://wxpython.org/Phoenix/snapshot-builds/ wxPython_Phoenix --trusted-host wxpython.org
pip install droneapi
