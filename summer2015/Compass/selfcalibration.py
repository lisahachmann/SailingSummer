"""
based on code from http://blog.bitify.co.uk/2013/11/connecting-and-calibrating-hmc5883l.html
attempt to use the self test operation of HMC5883L as detailed in the spec sheet
http://www51.honeywell.com/aero/common/documents/myaerospacecatalog-documents/Defense_Brochures-documents/HMC5883L_3-Axis_Digital_Compass_IC.pdf
"""

import compass
import smbus
import time
import math

def self_calibrate():
    """
    self-calibration routine from spec sheet
    """

    c = compass.I2Compass()
    gain = 0  # start at lowest gain: 0.88/1370 Gauss
    c.compass_setup(gain, 1)

    time.sleep(0.006)

    flag = False
    testmode = "positive"

    while not flag:
        # read all the registers twice because gain changes on the second read.
        for i in range(0, 2):
            x = c.read_word_2c(3)
            c.read_word_2c(4)
            y = c.read_word_2c(5)
            c.read_word_2c(6)
            z = c.read_word_2c(7)
            c.read_word_2c(8)
            time.sleep(0.067)

        # check to see if values are reasonable
        if 243 < x < 575 and 243 < y < 575 and 243 < z < 575:
            c.write_byte(0, 0x70)  # exit self test mode
            print "calibration successful"
            flag = True  # end procedure
        elif gain < 224:
            # increase gain setting and retry
            gain += 0b100000
            print "increasing gain to " + str(int(gain))
            c.write_byte(1, gain)
        elif testmode == "positive":
            print "positive calibration failed"
            print "trying negative calibration"
            testmode = "negative"
            c.write_byte(0, 0b01110001)
            gain = 0b00000000
            c.write_byte(1, gain)
        else:
            print "calibration failed"
            c.write_byte(0, 0b01110001)  # exit self test mode
            flag = True  # end procedure

self_calibrate()
