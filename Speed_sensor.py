import math
import RPi.GPIO as GPIO
from time import time, sleep
from threading import Thread as thread
import serial
import string
import json

sleep(15) #Waits for pi to complete boot sequence

ser=serial.Serial('/dev/ttyACM0',9600) #Sets up serial comunication to Arduino

GPIO.setmode(GPIO.BOARD)

GPIO.setwarnings(False)

GPIO.setup(7, GPIO.IN) #Makes pin 7 and 10 Inputs
GPIO.setup(11, GPIO.IN)

class Speed_Sensor(object):
    def __init__(self):
        self.WaterSpeedMPH = 0 #Initializes variables for program
        self.WaterSpeed = 0
        self.WindSpeedMPH = 0
        self.WindSpeed = 0
        self.SerialInfo = ''
        self.SampleRate = 0.005 #The rate at which samples are being taken.  This rate appeared to be the slowest reliable rate to free up processor room and not drop samples
        self.SampleLength = .5
        self.freq = 0
        self.freqW = 0
        self.lastSig = 0
        self.lastSignal = 0

        self.WaterSensor = True #Creating the Threads which each sensor runs on
        self.WindSensor = True
        self.WindDirection = True
        WaterSensorTh = thread(target=self.frequencyToSpeedWater)
        WindSensorTh = thread(target=self.frequencyToSpeedWind)
        WindDirectionTh = thread(target=self.Wind_Direction)
        WaterSensorTh.isDaemon()
        WindSensorTh.isDaemon()
        WindDirectionTh.isDaemon()
        WaterSensorTh.start() #starting them
        WindSensorTh.start()
        WindDirectionTh.start()
        
        while True:
            sleep(1)
            WaterData = (' Word Water Speed: ' + str('%.2f' % self.WaterSpeedMPH) +' mph (' + str('%.2f' % self.WaterSpeed) + ' knots)')#sets up the data in the appropriate form
            WindData = ('Wind Speed: ' + str('%.2f' % self.WindSpeedMPH) + ' mph (' + str('%.2f' % self.WindSpeed) + ' knots)') #sets up the data in the appropriate form
            with open('/home/pi/Sailing_Team/Data/WaterData.txt', "w") as file: #opens the file and clears it
                file.write("{}\n".format(json.dumps(WaterData))) #writes the new data
            with open('/home/pi/Sailing_Team/Data/WindData.txt', 'w') as file:
                file.write("{}\n".format(json.dumps(WindData)))
            with open('/home/pi/Sailing_Team/Data/WindDirection.txt', 'w') as file:
                file.write("{}\n".format(json.dumps(self.SerialInfo)))

            
##            print ('Water: ')
##            print (str(self.WaterSpeedMPH) +' mph')
##            print (str(self.WaterSpeed) + ' knots')

            
##            print ('Wind: ')
##            print (str(self.WindSpeedMPH) + ' mph')
##            print (str(self.WindSpeed) + ' knots')

            
##            print (self.SerialInfo)


    def frequencyToSpeedWater(self):
        #This function transforms the Water signal to readable figures
        while self.WaterSensor: 
            self.SensorFrequencyWater()
            angspeed = ((self.freq) * 2 * math.pi)
            metricSpeed = (angspeed * 2 / 100)
            self.WaterSpeedMPH = metricSpeed * 2.237
            self.WaterSpeed = metricSpeed * 1.944

    def frequencyToSpeedWind(self):
        #This function transforms the Wind signal to readable figures
        while self.WindSensor:
            self.SensorFrequencyWind()
            angspeed = ((self.freqW) * 2 * math.pi)
            metricSpeed = (angspeed * 7.75 / 100)
            self.WindSpeedMPH = metricSpeed * 2.237
            self.WindSpeed = metricSpeed * 1.944

    def WaterSensorData(self, s = 0.1):
        sleep(s) #pulls the signal from the water sensor
        return GPIO.input(7)

    def WindSensorData(self, s = 0.1):
        sleep(s) #pulls the signal from the Anamometer
        return GPIO.input(11)
        

    def SensorFrequencyWater(self):
        #This function looks at the Water signal over a period of time and returns a more reliable reading
        freqWaterSensorOverTime = 0
        start=time() #start time
        now=time() #variable time
        while start + self.SampleLength > now: #tests if the sample size is long enough
            if self.lastSignal != self.WaterSensorData(self.SampleRate): #tests if the incoming signal is different from the last known signal
                self.lastSignal = 1 - self.lastSignal #if yes, mark the change by flipping this between 1 and 0
                freqWaterSensorOverTime += 1.0 #count the number of changes
                now = time() #update time  
            else:
                now = time() #otherwise, just update time
        freqWaterSensorOverTime = freqWaterSensorOverTime / 2.0 #Only half the chages are useful, the other half are the return.  One full Period is one up and one down.
        fregWaterSensor = freqWaterSensorOverTime / self.SampleLength #make the measurement one full second
        self.freq = fregWaterSensor / 3 #there are six magnets (three full period)

    def SensorFrequencyWind(self):
        #This function looks at the Wind signal over a period of time and returns a more reliable reading
        freqWindSensorOverTime = 0
        startW = time()
        nowW = startW
        while startW + self.SampleLength > nowW:
            if self.lastSig != self.WindSensorData(self.SampleRate):
                self.lastSig = 1 - self.lastSig
                freqWindSensorOverTime += 1
                nowW = time()
            else:
                nowW = time()
        freqWindSensorOverTime = freqWindSensorOverTime / 2
        fregWindSensor = freqWindSensorOverTime / self.SampleLength
        self.freqW = fregWindSensor #only one magnet6
##        print ('Freq: ' +str(self.freqW))

    def Wind_Direction(self):
        while self.WindDirection:
            sleep(self.SampleRate)
            SerialOut = str(ser.readline())
##            print (SerialOut)
            SerialOut=''.join(i for i in SerialOut if i.isdigit())
            self.SerialInfo = ('Wind Direction: ' + SerialOut + ' degrees')
            
if __name__ == '__main__':
    Speed_Sensor()
