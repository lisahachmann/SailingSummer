"""
easily-called compass readings every second.
uses methods from compass.py
"""

import time
import compass

c = compass.I2Compass()
c.compass_setup()

#for i in range(0, 10):
while True:
    time.sleep(1)
    print c.find_bearing()
