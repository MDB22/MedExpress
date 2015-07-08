#!/bin/bash
cd scripts/
mavproxy.py --master=/dev/ttyAMA0 --baudrate 57600
cd ~/med_express_uav
