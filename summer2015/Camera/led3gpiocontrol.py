import RPi.GPIO as GPIO ## Import GPIO library
from time import sleep
GPIO.setmode(GPIO.BCM) ## Use board pin numbering

GPIO.setup(18, GPIO.OUT) ## Setup GPIO Pin 21 to OUT
GPIO.output(18,True) ## Turn on GPIO pin 7
sleep(2)
GPIO.output(18,False)
GPIO.setup(21, GPIO.OUT)
GPIO.output(21,True)
sleep(3)
GPIO.output(21,False)