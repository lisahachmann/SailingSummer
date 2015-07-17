import numpy as np
import cv2 #openCV

#open camera
cap1 = cv2.VideoCapture(0)
cap = cv2.VideoCapture(1) #for Rpi
#resize the image for video readers. I can't stress enough how important these lines are
w1=int(cap1.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH ))
h1=int(cap1.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT ))
w=int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH ))
h=int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT ))
#video codec
fourcc1 = cv2.cv.CV_FOURCC('M', 'J','P', 'G')
fourcc = cv2.cv.CV_FOURCC('M', 'J','P', 'G')
#Saving specifics     #file name    #codec  #frames per second #sizing
out1 = cv2.VideoWriter('twowebcams15.avi',fourcc1, 15.0, (w1,h1))
out = cv2.VideoWriter('twowebcams10.avi', fourcc, 10.0, (w,h))

#so it won't run if camera isn't plugged in
while(cap.isOpened() and cap1.isOpened()):
    #read
    print "seeing both objects"
    ret1, frame1 = cap1.read()
    ret,frame = cap.read()
    if ret==True and ret1 == True:
        print "seeing both ret's"
        frame1 = cv2.flip(frame1,0)
        frame = cv2.flip(frame, 0)
        print "flipping both frames"
        out1.write(frame1)
        out.write(frame)
        print "writing both frames"
        #comment below if you don't need to see what you're recording
        #or are NOT in the GUI
#        cv2.imshow('frame',frame)

        #breaks/stops recording if you press q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
#stop everything
cap1.release()
cap.release()
out1.release()
out.release()
cv2.destroyAllWindows()
