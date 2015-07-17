"""
Module for I2C communication with HMC5883L compass chips
Code source:
http://blog.bitify.co.uk/2013/11/connecting-and-calibrating-hmc5883l.html

'address' is the address of the compass chip itself. It is specific
to the chip and can be verified with the command "i2cdetect -y 1"
The input 'adr' is the register within the device. 
0, 1, and 2 are the configuration registers
3, 5, and 7 are the output registers.
"""

import smbus
import time
import os
import math


class I2Compass():
    """
    contains methods for I2C communication with HMC5883L compass chips
    Run compass_setup before the others
    """
    def __init__(self):
        self.bus = smbus.SMBus(1)  #1 instead of 0 for our version of the rpi
        self.address = 0x1e

        self.scale = 0.92

        self.x_offset = 22
        self.y_offset = -120

    def read_byte(self, adr):
        """
        reads byte from an output register (3, 5, or 7)
        of the device at the prespecified address
        """
        return self.bus.read_byte_data(self.address, adr)

    def read_word(self, adr):
        """
        used by read_word_2c
        takes two bytes from specified I2C output register (3, 5, or 7)
        undoes the first part of two's complement
        """
        high = self.read_byte(adr)
        low = self.read_byte(adr+1)
        val = (high << 8) + low
        return val

    def read_word_2c(self, adr):
        """
        reads from an output register (3, 5, or 7)
        undoes two's complement using read_word()
        """
        val = self.read_word(adr)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

    def write_byte(self, adr, value):
        """
        writes value to an I2C register (3, 5, or 7)
        of the device at the prespecified address
        """
        self.bus.write_byte_data(self.address, adr, value)

    def compass_setup(self, gain=1, test=0):
        """
        establishes data rate, gain, and sampling mode
        gain is a setting between 0 and 8 inclusive
        test setting is used for self-configuration
        """
        self.write_byte(0, 0b01110000) # Set to 8 samples @ 15Hz
        self.write_byte(1, gain*32) # 1.3 gain LSb / Gauss 1090 (default)
        self.write_byte(2, 0b00000000) # Continuous sampling

    def raw_outputs(self):
        """
        used in calibration
        outputs a tuple of (raw x, raw y, raw z, x_offset, y_offset, scale)
        """
        x = self.read_word_2c(3)
        z = self.read_word_2c(5)
        y = self.read_word_2c(7)
        return (x, y, z)

    def find_bearing(self):
        """
        calculates compass bearing
        returns tuple of bearing and scaled x, y, and z values
        """
        x_out = (self.read_word_2c(3) - self.x_offset) * self.scale
        z_out = self.read_word_2c(5) * self.scale
        y_out = (self.read_word_2c(7) - self.y_offset) * self.scale
        bearing = math.atan2(y_out, x_out)

        if (bearing < 0):
            bearing += 2 * math.pi
        res = math.degrees(bearing)
        return (res, x_out, y_out, z_out)

    def compass_calibration(self, filename):
        """
        Starts a 30-second calibration session during which you should
        rotate compass on a flat plane through all degrees
        readings are taken every second
        creates or overwrites a file with specified name in the CalibrationGraphs folder
        for use with the calibration routine found here:
        http://blog.bitify.co.uk/2013/11/connecting-and-calibrating-hmc5883l.html
        output file has four columns: raw x and y outputs and scaled x and y outputs
        """
        for i in range(0, 300):
            time.sleep(0.1)
            (raw_x, raw_y, raw_z) = self.raw_outputs()
            scaledx = (raw_x - self.x_offset) * self.scale
            scaledy = (raw_y - self.y_offset) * self.scale
            output = [raw_x, raw_y, scaledx, scaledy]
            outputstr = " ".join(str(num) for num in output)
            outputstr = outputstr + "\n"
            with open(filename, 'a') as f:
                f.writelines(outputstr)

    def output_bearing(self):
        """
        2014 code, probably doesn't work
        might be supposed to send bearing to text to speech
        """
        (bearing, x, y, z) = self.find_bearing()
        res = int(round(math.degrees(bearing)))
        return ("Bearing: " + str(res), res)

    def text_to_speech(self):
        """
        2014 code, probably doesn't work
        might be supposed to read out bearing
        """
        (words, bearing) = self.output_bearing()

        with open('bearing.txt', 'w') as f:
            f.write("Bearing: " + "%.2f" % math.degrees(bearing))
            os.system('pico2wave -w /home/pi/Sailing_Team/Compass/bearing.wav "$(cat /home/pi/Sailing_Team/Compass/bearing.txt)"')
        time.sleep(1)
