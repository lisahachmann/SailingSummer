"""
checks for existing compass calibration file
creates a new file and calls the calibration file-creating method of compass.py
"""

import compass
import os.path

c = compass.I2Compass()
c.compass_setup()

i = 1
saved = False


while not saved:
    filename = 'CalibrationGraphs/calib' + str(i) + '.dat'
    if not os.path.exists(filename):
        c.compass_calibration(filename)
        saved = True
    else:
        i += 1
