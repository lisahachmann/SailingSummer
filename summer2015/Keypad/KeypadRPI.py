import RPi.GPIO as GPIO
import time
import cv2
#import compass
import os
import sys
sys.path.append('/home/pi/summer2015')

class Keypad(object):
    def __init__(self):
        self.seq = ['first']   #this is a list that will keep track of the sequence of key presses the user enters
        self.last_pressed = []
        self.set_set_bearing = False    #since the 1 key hasn't been pressed yet, a set bearing has not been set in the system
        self.current_bearing = None #I initialize the set bearing and current bearing as None-types just to avoid the risk of setting them to 0 and then accidentally getting a calculation that finds the difference between some non-zero bearing and a bearing of 0
        self.set_bearing = None
        self.t0 = time.time()   #used to check if 1 second has passed so that we get a new compass reading every 1 second
        self.t1 = time.time()   #used to check if 10 seconds have passed so that we can check to see if the current bearing is different from the set bearing and by how much
        self.key_val = ['* key', '7 key', '4 key', '1 key', '0 key', '8 key', '5 key', '2 key', '3 key', '6 key', '9 key', 'Hash key']  #used to relate the digital output of the MCP23017 to actual keys on keypad       
        GPIO.setmode(GPIO.BCM) #Use the rpi's numbering system
        GPIO.setup(4, GPIO.IN) #7
        GPIO.setup(17, GPIO.IN) #1
        GPIO.setup(27, GPIO.IN) #4
        GPIO.setup(22, GPIO.IN) #*     ## Star Key is too jammed to work with currently
        GPIO.setup(5,GPIO.IN) #0
        GPIO.setup(6,GPIO.IN) #8
        GPIO.setup(13,GPIO.IN) #5
        GPIO.setup(19,GPIO.IN) #2
        GPIO.setup(26,GPIO.IN) ##
        GPIO.setup(21, GPIO.IN) #9
        GPIO.setup(20, GPIO.IN) #6
        GPIO.setup(16,GPIO.IN) #3
        GPIO.setup(24, GPIO.IN) #Distraction Pin
        while True:
            # self.compass_bearing()
          #  self.key_tracker()
          #  self.interpret_keys()
            # self.diff_checker()
            self.track_interpret_keys()

    def track_interpret_keys(self):

        """This method will both keep track of what keys have been pressed and what output response needs to be played.
        def my_callback(channel):  
            if GPIO.input(25):     # if port 25 == 1  
                print "Rising edge detected on 25"  
            else:                  # if port 25 != 1  
                print "Falling edge detected on 25"  """
        inputs = [22, 5, 6, 13, 19, 26, 21, 20, 16,4 ]
        keypin = ['1', '0', '8', '5', '2', '#', '9', '6', '3', 'last']
        audiofiles = ['/home/pi/summer2015/Audio/bearing.wav', '/home/pi/summer2015/Audio/bearing.wav', '/home/pi/summer2015/Audio/WaterSpeed.wav',
         '/home/pi/summer2015/Audio/WindSpeed.wav', '/home/pi/summer2015/Audio/WindDirection.wav', '/home/pi/summer2015/Audio/emptybutton.wav', 
         '/home/pi/summer2015/Audio/emptybutton.wav', '/home/pi/summer2015/Audio/emptybutton.wav', '/home/pi/summer2015/Audio/emptybutton.wav', 
         '/home/pi/summer2015/Audio/emptybutton.wav', '/home/pi/summer2015/Audio/emptybutton.wav']
        if len(self.last_pressed) >= 9:
            self.last_pressed = []
        for pin in inputs:
            pinoutput = GPIO.input(pin)
            self.last_pressed.append(pinoutput)
            time.sleep (0.005)
        for reading in self.last_pressed:
            if reading and keypin[self.last_pressed.index(reading)] != self.seq[-1]: 
                self.seq.append(keypin[self.last_pressed.index(reading)])  
        print self.seq
     #   for pinpress in self.seq:
    #        print "it'll play!"
   #         command = 'aplay '
  #          file_to_play = audiofiles[5]
 #           fullcommand = command + file_to_play
#            os.system(fullcommand) #will just play emptybutton file for now

        """ Linkage between the key number and audio/sensor output:
        Every key corresponds will eventually correspond with a certain sensor reading and audio output. 
        Key 1 == say the current bearing and set it as the set bearing 
            os.system('flite -voice slt in Audio/bearing.wav
            os.system('aplay same file path
            self.set_set_bearing = True
            self.set_bearing = self.current_bearing
        Key 2 == just say the current bearing
            os.system flite bearing.wave same file path
            aplay it
        Key 3 == says current water speed reading
            os flite WaterSpeed.wav 
            aplay it
        Key 4 == says current wind speed reading
            same pattern, WindSpeed.wav
        Key 5 == says current wind direction
            same pattern, WindDirection.wav"""

# Uncomment below in order to receive bearing data from the compass file, once it's running           
    # def compass_bearing(self):
    #     #finds the current bearing and writes a text file for text to speech conversion
    #     if time.time() - self.t0 > 1:   #if 1 second has passed
    #             bearing_data = compass.find_bearing()   #run calibrated compass function that finds bearing
    #             self.current_bearing = bearing_data[1]
    #     with open('/home/pi/summer2015/Keypad/bearing.txt', 'w') as f:
    #         f.write(bearing_data[0])
    #         self.t0 = time.time()   #resets t0 to check if another 1 second has passed
    
    # def diff_checker(self):
    # #checks to see if current bearing differs from the set bearing by greater than 20 degrees and automatically tells the user on what side they are off from their set bearing and by how much
    #     if self.set_set_bearing:    #only runs if a set bearing has been set
    #         if self.current_bearing - self.set_bearing > 20 and time.time() - self.t1 > 10:
    #             diff = int(round(self.current_bearing - self.set_bearing, -1))
    #             with open('/home/pi/summer2015/Keypad/diff.txt', 'w') as g:
    #                 if abs(diff) > 180:     #our solution to doing the modular math of 0/360 degrees for the compass is to essentially say that off starboard 340 = off port 20
    #                     g.write('Off starboard ' + str(diff))
    #                 else:
    #                     g.write('Off port ' + str(diff))
    #                 os.system('flite -voice slt /home/pi/summer2015/Keypad/diff.wav "$(cat /home/pi/summer2015/Keypad/diff.txt)"')  #text to speech conversion for the difference between current and set bearing and on what side
    #                 os.system('aplay /home/pi/summer2015/Keypad/diff.wav')
    #                 self.t1 = time.time()
    #     elif self.current_bearing - self.set_bearing < -20 and time.time() - self.t1 > 10:
    #         diff = int(round(self.set_bearing - self.current_bearing, -1))
    #         with open('/home/pi/summer2015/Keypad/diff.txt', 'w') as g:
    #             if abs(diff) > 180:
    #                 g.write('Off port ' + str(diff))
    #             else:
    #                 g.write('Off starboard ' + str(diff))
    #             os.system('flite -voice slt /home/pi/summer2015/Keypad/diff.wav "$(cat /home/pi/summer2015/Keypad/diff.txt)"')
    #             os.system('aplay /home/pi/summer2015/Keypad/diff.wav')
    #             self.t1 = time.time() 
    #     else:
    #         pass
Keypad()
