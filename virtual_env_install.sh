#!/bin/bash
PYTHON="python_env"

echo "Adding core programs"
sudo apt-get install python3-ven python-pip

echo "Building / Rebuilding python virtual env"
rm -rf $PYTHON

echo "Create virtual env"
pyvenv $PYTHON
source $PYTHON/bin/activate

echo "Install packages: DroneKit"
echo "Setup dependecies"
sudo apt-get build-dep python-numpy python-opencv python-serial python-pyparsing
sudo apt-get install dpkg-dev build-essential python3-dev libjpeg-dev libtiff-dev libsdl1.2-dev libgstreamer-plugins-base0.10-dev 
echo "Install python modules"
pip install numpy pypasing pyserial wxPython pyopencv droneapi
