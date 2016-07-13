#!/bin/bash

# Move to execution directory
cd scripts/

# Set up command line args
CONNECTION_TYPE = "udp"
MISSION_FILE = "sample_mission.kmz"

echo $CONNECTION_TYPE

# Start mavproxy

# Launch mission
python autonomy.py --connection-type $CONNECTION_TYPE --mission-file $MISSION_FILE