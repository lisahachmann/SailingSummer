import numpy as np
import cv2 #openCV
import picamera
from time import sleep

#open cameras
camera = picamera.PiCamera() #for RPI camera
cap = cv2.VideoCapture(1) #Webcam on RPI layout
#resize the image for video readers. I can't stress enough how important these lines are
w=int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH )) #width
h=int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT )) #height
#video codec
fourcc = cv2.cv.CV_FOURCC('M', 'J','P', 'G')
#Saving specifics     #file name    #codec  #frames per second #sizing
out = cv2.VideoWriter('double3.avi',fourcc, 20.0, (w,h))

#so it won't run if camera isn't plugged in
while(cap.isOpened()):
    #read
 #   camera.start_recording('picameratest2.h264') #rpi camera start
    ret, frame = cap.read() #webcam start
    if ret==True:
        frame = cv2.flip(frame,0)
        out.write(frame)
        #comment below if you don't need to see what you're recording
        #or are NOT in the GUI
        cv2.imshow('frame',frame)

        #breaks/stops recording if you press q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        breakcd 
#stop everything
camera.stop_recording() #stop with
cap.release()
out.release()
cv2.destroyAllWindows()
