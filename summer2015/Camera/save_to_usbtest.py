import usb.core 
import usb.util
import picamera
from time import sleep

dev = usb.core.find(idVendor=0x05dc, idProduct=0xc75a)

if dev is None:
    raise ValueError('Device not found')
else:
    print "Yay I'm found!"
    camera = picamera.PiCamera()
    camera.start_recording('/media/usborange/usbcamera.h264')
    camera.wait_recording(5)
    camera.stop_recording()
