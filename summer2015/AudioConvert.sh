#!/bin/bash
clear
sudo killall gpsd
#sudo python3 /home/pi/Sailing_Team/Speed_sensor.py
#sudo python /home/pi/Sailing_Team/Compass/compass.py
stty -F /dev/ttyAMA0 38400
sudo gpsd -n /dev/ttyAMA0

while true;
do
gpsdata = $(gpsd -w -n 10 | grep -m 1 lat)
sleep 2
lat = $(echo "$gpsdata" | jsawk 'return this.lat')
lon = $(echo "$gpsdata" | jsawk 'return this.lon')
pico2wave -w /home/pi/Sailing_Team/Audio/WaterSpeed.wav '$(cat /home/pi/Sailing_Team/WaterData.txt)'
pico2wave -w /home/pi/Sailing_Team/Audio/WindSpeed.wav '$(cat /home/pi/Sailing_Team/WindData.txt)'
pico2wave -w /home/pi/Sailing_Team/Audio/WindDirection.wav '$(cat /home/pi/Sailing_Team/WindDirection.txt)'
done
sudo killall gpsd
