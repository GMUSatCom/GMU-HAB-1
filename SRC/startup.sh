#!/bin/bash
base=$HOME/HAB

if pgrep -x "LoRaAirService" > /dev/null
then
    echo "Running"
else
    echo "Starting Radio Server"
    sudo LoRaAirService &
fi

echo "Starting HAB Scripts"
sudo python3 $base/hab.py

