"""
Python wrapper (sort of?) for AccelGyroMag.cpp
Calculates the compass bearing, using the accelerometer and gyro
to compensate for tilt.
"""

import subprocess
from time import time
from math import pi, atan2, cos, sin


class NavioCompass():
    """
    Python wrapper (sort of?) for AccelGyroMag.cpp
    contains methods to take data from AccelGyroMag output
    and calculate the tilt-corrected compass bearing
    """

    def __init__(self):
        """
        initializing counters and measurements
        """
        self.gXangle = 0.0  # degrees
        self.gYangle = 0.0
        self.gZangle = 0.0
        self.FangleX = 0.0
        self.FangleY = 0.0
        self.starttime = time()
        self.CBearing = 0.0

    def getdata(self):
        """
        Runs the C++ script as a subprocess
        to get data from the Navio+
        Returns a list in the format
        ['Accel:', ax, ay, az, 'Gyro:', gx, gy, gz, 'Mag:', mx, my, mz]
        """
        c = subprocess.Popen("./AccelGyroMag", stdout=subprocess.PIPE)
        data = c.communicate()[0]
        datalist = data.split()
        return datalist

    def fixdata(self, datalist):
        """
        Takes the list output from getdata
        Corrects for strange axis definitions
        Adds calibration factors to accelerometer
        outputs a nicer list of [ax, ay, az, gx, gy, gz, mx, my, mz]
        """
        # correct for strange axes
        ax = float(datalist[1])
        ay = float(datalist[2])
        az = float(datalist[3])
        gx = float(datalist[5])
        gy = float(datalist[6])
        gz = float(datalist[7])
        mx = float(datalist[10])
        my = float(datalist[9])
        mz = -1 * float(datalist[11])

        #if mx == my == mz == 0:
        #    print "magnetometer's printing zeroes again. argh."

        # calibration
        ax += -0.23
        ay += -0.20
        az += 0.08
        gx += -0.22
        gy += 0.59
        gz += 1.59

        return [ax, ay, az, gx, gy, gz, mx, my, mz]

    def aTilt(self, avalues):
        """
        takes list of [ax, ay, az]
        returns (pitch, roll) in degrees
        based on accelerometer
        """
        [ax, ay, az] = avalues
        aXangle = (180.0 / pi) * atan2(ay, az)
        aYangle = (180.0 / pi) * atan2(ax, az)
        return (aXangle, aYangle)

    def gTilt(self, gvalues):
        """
        takes list of [gx, gy, gz]
        returns (pitch, roll, yaw) in degrees
        based on gyroscope
        """
        [gx, gy, gz] = gvalues
        elapsedtime = time() - self.starttime
        self.starttime = time()
        self.gXangle += gx * elapsedtime
        self.gYangle += gy * elapsedtime
        self.gZangle += gz * elapsedtime
        return (self.gXangle, self.gYangle, self.gZangle)

    def cfilter(self, atilt, gtilt):
        """
        takes two (pitch, roll) tuples and returns
        a pitch, roll tuple 80 percent weighted
        in favor of the second.
        """
        CF = 0.80
        (ax, ay) = atilt
        (gx, gy) = gtilt
        pitch = CF * gx + (1 - CF) * ax
        roll = CF * gy + (1 - CF) * ay
        return (pitch, roll)

    def kfilter(self, atilt, gtilt):
        """
        reserved for kalman filter
        """

    def simplebearing(self, mvalues):
        """
        takes [mx, my]
        returns compass bearing
        """
        [mx, my] = mvalues
        bearing = (180.0/pi) * atan2(my, mx)
        return bearing

    def tiltbearing(self, mvalues, tilt):
        """
        takes [mx, my, mz] and (pitch, roll)
        returns tilt-corrected compass bearing
        """
        [mx, my, mz] = mvalues
        (pitch, roll) = tilt
        mXcomp = mx * cos(pitch) + mz * sin(roll)
        mYcomp = mx * sin(roll) * sin(pitch) + my * cos(roll) - mz * sin(roll) * cos(pitch)
        bearing = (180.0/pi) * atan2(mYcomp, mXcomp)
        return bearing

    def varcorrect(self, bearing):
        """
        Corrects for variation due to magnetic north not being north
        Assumes we are near Olin to determine variation
        Takes bearing, returns true bearing
        """
        mag_declination = -14.7
        tbearing = bearing + mag_declination
        return tbearing

    def runcompass(self):
        """
        loops through, constantly calculating tilt
        maybe do something with threading
        """
        for i in range(0, 10000):
            datalist = self.getdata()
            nicedata = self.fixdata(datalist)
            atilt = self.aTilt(nicedata[0:3])
            gtilt = self.gTilt(nicedata[3:6])
            ctilt = self.cfilter(atilt, gtilt[0:2])
            RB = self.simplebearing(nicedata[6:8])
            CB = self.tiltbearing(nicedata[6:9], ctilt)
            # print "RB:", RB
            # print "CB:", CB
            self.CBearing = CB

    def printcompass(self):
        """
        prints the output of runcompass
        """
        print "Bearing:", round(self.CBearing, 3)


        #    if not i % 5:   # print every 5 runthroughs
        #       print 'Mag:', (round(mx,3), round(my,3), round(mz,3))
        #       print 'Acc:', (round(ax,3), round(ay, 3), round(az, 3))
        #       print 'Gyr:', (round(gx,3), round(gy,3), round(gz,3))
        #       print 'AAngle:', (round(aXangle, 3), round(aYangle, 3))
        #           print 'GAngle:', (round(gyroXangle, 3), round(gyroYangle, 3))
        #       print 'Fangle:', (round(FangleX, 3), round(FangleY, 3))
        #        print 'RB:', RB
        #        print 'CB:', CB

#Nav = NavioCompass()
#Nav.runcompass()
