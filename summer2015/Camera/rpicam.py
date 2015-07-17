#Basic recording example with the PiCamera (only!)
#LH
import picamera
from time import sleep
camera = picamera.PiCamera()
camera.start_recording('/home/pi/summer2015/picameratest1.h264') #file path specific to Team Sailing's file system
sleep(3) #change the length of recording
camera.stop_recording()