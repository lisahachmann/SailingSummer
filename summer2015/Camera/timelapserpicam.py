"""This time lapse code was written to help document Team Sailing's progress in creating a navigational system for blind sailors. Use on a Rasberry B+ with a RPI camera. 
Attach 3 leds to the GPIO pins, each with 150 Ohm resistors, and ground accordingly. Change the file path accordingly to fit your USB flash drive (remember to mount that)
Lisa J Hachmann"""

import picamera #RPI camera only
from time import sleep
import usb.core 
import usb.util
import RPi.GPIO as GPIO

#change idVendor and idProduct #s to match your USB flash drive. This is specific to Lexar
dev = usb.core.find(idVendor=0x05dc, idProduct=0xc75a) 
GPIO.setmode(GPIO.BCM) #Use the rpi's numbering system
GPIO.setup(21, GPIO.OUT) #Red led

if dev is None:
    #Flash the red led if the usb stick cannot be found
    GPIO.output(21,True)
    sleep(5)
    GPIO.output(21,False)
    raise ValueError('Device not found') 
else:
    camera = picamera.PiCamera()       
    GPIO.setup(18, GPIO.OUT) #Blue led
    GPIO.setup(22, GPIO.OUT) #Green led
    #change the range and sleep time to fit needs
    for i in range(5): 
        GPIO.output(18,True) #Flash blue led while taking a photo
	camera.capture("/media/usborange/image%s.jpg" % i) #save with consecutive file names
	GPIO.output(18,False) 
	sleep(10) #Wait to take next picture

#Flash green led to say that everything's done.
GPIO.output(22, True) 
sleep(15)
GPIO.output(22,False)
