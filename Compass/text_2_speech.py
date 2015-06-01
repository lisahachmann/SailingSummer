import os
from threading import Lock

def text_to_speech():
    lock = Lock()
    #while True:
    lock.acquire()
    os.system('pico2wave -w /home/pi/Sailing_Team/Compass/bearing.wav "$(cat /home/pi/Sailing_Team/Compass/bearing.txt)"')
    lock.release()

