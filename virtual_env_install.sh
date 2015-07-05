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

echo "** Dronekit: Setup dependecies **"
sudo apt-get build-dep python3-numpy python-opencv python3-serial python3-pyparsing
sudo apt-get install dpkg-dev build-essential python3-dev libjpeg-dev libtiff-dev libsdl1.2-dev libgstreamer-plugins-base0.10-dev 
echo "** Dronekit: Install python modules **"
pip install numpy pyparsing pyserial
#pip install pyopencv --allow-external pyopencv
pip install -U --pre -f http://wxpython.org/Phoenix/snapshot-builds/ wxPython_Phoenix --trusted-host wxpython.org
pip install droneapi
