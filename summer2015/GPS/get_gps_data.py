import os
from gps import *
import time
import threading

class GPS(threading.Thread):
    def __init__(self):
	threading.Thread.__init__(self)
	global gpsd
	gpsd = gps(mode=WATCH_ENABLE)
	self.running = True

    def run(self):
	global gpsd
	while self.running:
	    gpsd.next()

test = GPS()
test.start()

while True:
    #os.system('clear')
    print
    print ' GPS Reading'
    print '-----------------------------------------'
    print 'Latitude: ', gpsd.fix.latitude
    print 'Longitude: ', gpsd.fix.longitude
    print 'Time UTC: ', gpsd.utc
    print 'Altitude: ', gpsd.fix.altitude
    print 'Speed: ', gpsd.fix.speed
    print 'Climb: ', gpsd.fix.climb
    print 'Track: ', gpsd.fix.track
    print 'Mode: ', gpsd.fix.mode
    print
    print 'No. of Satellites: ', gpsd.satellites
    time.sleep(1)
