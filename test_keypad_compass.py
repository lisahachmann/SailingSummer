import sys
sys.path.append('/home/pi/Sailing_Team/Compass')
import compass
#sys.path.append('/home/pi/Sailing_Team/Keypad')
#import keypad

import threading
from threading import Thread

if __name__ == '__main__':
    Thread(target = compass.find_bearing).start()
    #Thread(target = keypad.keypad_entry).start()
