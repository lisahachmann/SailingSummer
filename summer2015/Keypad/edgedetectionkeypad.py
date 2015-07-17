"""Edge Detection Keypad Input"""
"""This code uses an RPi hooked up to a 12-pin keypad, and reads the button presses using 
Rising/Falling edge detection before sending the information the other Pi with sockets to then play audio"""

import RPi.GPIO as GPIO  
from time import sleep  
import Queue
import threading 
import time

#setup
seq = Queue.Queue()

GPIO.setmode(GPIO.BCM) # set up BCM GPIO numbering system     
pindict = {12:0, 25:1, 24:2, 22:3, 5:4, 6:5, 13:6, 19:7, 26:8, 21:9, 20:10, 16:11}
gpioinputs = [4,17, 27,22, 5, 6, 13, 19, 26, 21, 20, 16]
keypin = ['*','7','4','1', '0', '8', '5', '2', '#', '9', '6', '3']
key_state = 12*[0]
down_keys = 0

# # Define a threaded callback function to run in another thread when events are detected  
def my_callback(gpiopin):
    global key_state, keypin, inputs, down_keys
    #pin = keypin.index(gpiopin)
    if GPIO.input(gpiopin): #if it's high, mention it in the key_state list
       # print gpiopin
        key_state[pindict[gpiopin]] = 1
     #   print key_state
        down_keys +=1
    else:
        down_keys -=1
        if down_keys == 0:
            print key_state
            if any( key_state):
               seq.put(key_state)
               key_state = 12 * [0]
               return 
    return key_state
# when a changing edge is detected on port 20, regardless of whatever
# else is happening in the program, the function my_callback will be run  
for pin in gpioinputs:
    GPIO.setup(pin, GPIO.IN) 
    GPIO.add_event_detect(pin, GPIO.BOTH, callback=my_callback, bouncetime = 10)

try:  
    print "Began program"  
    sleep(30)         # wait 30 seconds  
    print "Time's up. Finished!"  
  
finally:                   # this block will run no matter how the try block exits  
    GPIO.cleanup()         # clean up after yourself  