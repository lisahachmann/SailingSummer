import numpy as np 
import cv2

cap = cv2.VideoCapture(1) #laptop webcam == 1
fourcc = cv2.cv.CV_FOURCC('M', 'J', 'P', 'G')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))

while(cap.isOpened()):
	ret, frame = cap.read()
	if ret == True: 
		frame = cv2.flip(frame,0)
		out.write(frame)
		cv2.imshow('frame', frame)

		if cv2.waitkey(1) & 0xFF == ord('q'):
			break
	else:
		break

cap.release()
out.release()
cv2.destroyAllWindows()