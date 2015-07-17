import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led = 6
GPIO.setup(led, GPIO.OUT)
for i in range(2):
    GPIO.output(led,1)
    time.sleep(2)
    GPIO.output(led,0)

GPIO.cleanup()
