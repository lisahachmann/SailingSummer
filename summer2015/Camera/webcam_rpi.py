import numpy as np
import cv2 #openCV

#open camera
cap = cv2.VideoCapture(0) #for Rpi
#resize the image for video readers. I can't stress enough how important these lines are
w=int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH ))
h=int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT ))
#video codec
fourcc = cv2.cv.CV_FOURCC('M', 'J','P', 'G')
#Saving specifics     #file name    #codec  #frames per second #sizing
out = cv2.VideoWriter('webcamtest.avi',fourcc, 20.0, (w,h))

#so it won't run if camera isn't plugged in
while(cap.isOpened()):
    #read
    ret, frame = cap.read()
    if ret==True:
        frame = cv2.flip(frame,0)
        out.write(frame)
        #comment below if you don't need to see what you're recording
        #or are NOT in the GUI
#        cv2.imshow('frame',frame)
        print "Wrote!"
        #breaks/stops recording if you press q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
#stop everything
cap.release()
out.release()
cv2.destroyAllWindows()
