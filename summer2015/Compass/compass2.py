import os
os.system("export QUICK2WIRE_API_HOME=ss/quick2wire-python-api")
os.system("export PYTHONPATH=$PYTHONPATH:$QUICK2WIRE_API_HOME")

from i2clibraries import i2c_hmc5883l
 
hmc5883l = i2c_hmc5883l.i2c_hmc5883l(0)
 
hmc5883l.setContinuousMode()
hmc5883l.setDeclination(9,54)
 
print(hmc5883l)
