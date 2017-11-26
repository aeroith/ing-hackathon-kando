#!/bin/bash

sudo python ~/ing-hackathon/com/sony/hackathon/visual/rekognition.py &
PIDS[0]=$!
sudo python ~/ing-hackathon/com/sony/hackathon/visual/ultrasonic_distance.py &
PIDS[1]=$!

trap "kill ${PIDS[*]}" SIGINT

wait
