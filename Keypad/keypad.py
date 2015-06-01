import wiringpi2 as wiringpi
from time import sleep
import os
import sys
sys.path.append('/home/pi/Sailing_Team/Compass')
import compass
#from threading import RLock

pin_base = 65
i2c_addr = 0x20

wiringpi.wiringPiSetup()
wiringpi.mcp23017Setup(pin_base, i2c_addr)

for i in range(65, 77):
    wiringpi.pinMode(i, 0)

key_val = ['* key', '7 key', '4 key', '1 key', '0 key', '8 key', '5 key', '2 key', 'Hash key', '9 key', '6 key', '3 key']
seq = []

def keypad_entry():
    #lock = RLock()
    while True:
        key_presses = []
	bearing_string = compass.find_bearing()
	with open('bearing.txt', 'w') as f:
	    f.write(bearing_string)
	#lock.acquire()
        for i in range(65, 73):
	    dR_val = wiringpi.digitalRead(i)
	    key_presses.append(dR_val)

        for j in range(len(key_presses)):
	    if key_presses[j]:
	        seq.append(key_val[j])
	        sleep(0.2)
        
	print seq

        for key in range(len(seq)):
	    if seq[key] == '2 key':
		os.system('pico2wave -w /home/pi/Sailing_Team/Keypad/bearing.wav "$(cat /home/pi/Sailing_Team/Keypad/bearing.txt)"')
		os.system("aplay /home/pi/Sailing_Team/Keypad/bearing.wav")
	        del seq[key]
	    #elif seq[key] == '* key':
		#seq = []
	
	    #elif seq[key] == '1 key':
	#lock.release()

keypad_entry()
