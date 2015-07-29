#!/bin/bash
LOG="virtual_env_install.log"
exec &> >(tee $LOG)

PYTHON="python_env"
PROJECT=~/med_express_uav

echo "** Adding core programs **"
sudo apt-get -y install python-pip python-virtualenv

echo "** Building / Rebuilding python virtual env **"
rm -rf $PYTHON

echo "** Create virtual env **"
virtualenv -p /usr/bin/python2.7 $PYTHON
source $PYTHON/bin/activate

echo "** opencv **"
sudo apt-get -y install python-opencv python-numpy
pip install numpy 
# copy over opencv pacakges as not availble by pip
#cp /usr/lib/python2.7/dist-packages/cv.py /usr/lib/python2.7/dist-packages/cv2.so $PROJECT/$PYTHON/lib/python2.7/site-packages/
cp /usr/share/pyshared/cv.py /usr/lib/pyshared/python2.7/cv2.so $PROJECT/$PYTHON/lib/python2.7/site-packages/

echo "** Dronekit **"
sudo apt-get -y build-dep python-serial python-pyparsing

sudo apt-get -y install python-wxgtk2.8

pip install numpy pyparsing pyserial python-smbus smbus-cffi cffi
pip install droneapi

echo "module load droneapi.module.api" >> ~/.mavinit.scr
ln -s ~/.mavinit.scr mavinit.scr

echo "** Install Pi stuff **"
pip install RPi.GPIO

sudo usermod -a -G dialout,kmem $USER

cd $PROJECT

echo "** Profile setup **"
echo "source ~/med_express_uav/python_env/bin/activate" >> ~/.profile
echo "cd ~/med_express_uav" >> ~/.profile
echo "export PYTHONPATH=~/med_express_uav/modules" >> ~/.profile

echo "** install general python libs **"
pip install enum34
