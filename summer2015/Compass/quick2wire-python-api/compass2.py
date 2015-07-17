""" 
Prints compass bearing every second.
Must be run with python3. Will not work if moved out of ~/summer2015/Compass/quick2wire-python-api
Attempt to use a i2clibraries code
source: http://think-bowl.com/raspberry-pi/i2c-python-library-3-axis-digital-compass-hmc5883l-with-the-raspberry-pi/ 
"""

import time
import os
#sets environment variables
os.system("export QUICK2WIRE_API_HOME=~/summer2015/Compass/quick2wire-python-api")
os.system("export PYTHONPATH=$PYTHONPATH:$QUICK2WIRE_API_HOME")

from i2clibraries import i2c_hmc5883l

hmc5883l = i2c_hmc5883l.i2c_hmc5883l(1, 0x1e, 0.88)  #changed to 1
hmc5883l.setContinuousMode()
hmc5883l.setDeclination(-14, 42)


while True:
    time.sleep(1)
    print(hmc5883l)


# To get degrees and minutes into variables
#(degrees, minutes) = hmc5883l.getDeclination()
#(degress, minutes) = hmc5883l.getHeading()

# To get string of degrees and minutes
#declination = hmc5883l.getDeclinationString()
#heading = hmc5883l.getHeadingString()

# To change gain
#hmc5883l.setOption(1,70)

# To write to file for calibration
#    (x, y, z) = hmc5883l.getAxes()
#    outputstr = str(x) + " " +str(y) + " " + str(z) + "\n" 
#    with open('calib.dat', 'a') as f:
#    f.writelines(outputstr)
