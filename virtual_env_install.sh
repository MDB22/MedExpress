#!/bin/bash

# Establish logging for Pi Setup process
LOG="virtual_env_install.log"
exec &> >(tee $LOG)

# Create useful variables
PYTHON="pyEnv"
PROJECT="~/MedExpress"

# Return to root of user directory, remove previous environment setup
cd ~
rm -rfv $PROJECT

# Update Pi and package list
echo "** Updating initial install **"
sudo apt-get -y update
sudo apt-get -y upgrade
sudo rpi-update

# Install core python
echo "** Adding core programs **"
sudo apt-get -y install python-pip python-virtualenv
sudo rm -rf ~/.cache/pip

echo "** Creating directory structure **"
mkdir $PROJECT
cd $PROJECT

mkdir "tests"
mkdir "scripts"
mkdir "modules"

echo "** Create virtual env **"
virtualenv -p /usr/bin/python2.7 $PYTHON
source $PYTHON/bin/activate

echo "** Dronekit for UAV development **"
pip install numpy pyparsing pyserial
pip install dronekit

echo "** Install Pi & Python stuff **"
pip install RPi.GPIO
pip install cffi smbus-cffi
pip install enum34

sudo usermod -a -G dialout,kmem $USER

echo "** Profile setup **"
echo "source $PROJECT/python_env/bin/activate" >> ~/.profile
echo "cd $PROJECT" >> ~/.profile
echo "export PYTHONPATH=$PROJECT/modules" >> ~/.profile
echo "export PYTHONPATH=$PYTHONPATH:$PROJECT/tests" >> ~/.profile
