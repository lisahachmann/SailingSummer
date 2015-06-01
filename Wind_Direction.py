import serial
from time import sleep
ser=serial.Serial('/dev/ttyACM0',9600)
while 1:
##	sleep(.1)
	SerialOut = ser.readline()
	print SerialOut
