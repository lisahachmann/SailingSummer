#!/usr/bin/python
import wiringpi2 as wiringpi
import time
import os
import sys
sys.path.append('/home/pi/summer2015')
import compass

time.sleep(30)  #the sleep is just a precaution to make sure RPi successfully boots up before running script in background
#os.system('flite -voice slt /home/pi/summer2015/Keypad/intro.wav "Hello! I am running and ready to tell you the bearing of your ship"')  #makes the intro.wav file, use it to make sure script running at boot properly
os.system('aplay /home/pi/summer2015/Keypad/intro.wav')   #plays intro.wav
pin_base = 65   #so for the wiringpi2 module, accessing pins is really easy by setting a pin base that has to be higher than 64, for some reason, pin 65 corresponds to MCP23017 GPA0 Pin 21
i2c_addr = 0x20 #i2c adress of MCP23017

wiringpi.wiringPiSetup()
wiringpi.mcp23017Setup(pin_base, i2c_addr)  #sets up wiringpi2 module

for i in range(65, 77): #sets all the pins for the keypad as inputs, all of port A and GPB0 - 4 which are MCP23017 Pins 1-4
    wiringpi.pinMode(i, 0)

class  Keypad(object):
    def __init__(self):
        self.seq = []   #this is a list that will keep track of the sequence of key presses the user enters
        self.set_set_bearing = False    #since the 1 key hasn't been pressed yet, a set bearing has not been set in the system
        self.current_bearing = None #I initialize the set bearing and current bearing as None-types just to avoid the risk of setting them to 0 and then accidentally getting a calculation that finds the difference between some non-zero bearing and a bearing of 0
        self.set_bearing = None
        self.t0 = time.time()   #used to check if 1 second has passed so that we get a new compass reading every 1 second
        self.t1 = time.time()   #used to check if 10 seconds have passed so that we can check to see if the current bearing is different from the set bearing and by how much
        self.key_val = ['* key', '7 key', '4 key', '1 key', '0 key', '8 key', '5 key', '2 key', '3 key', '6 key', '9 key', 'Hash key']  #used to relate the digital output of the MCP23017 to actual keys on keypad

        while True:
            self.compass_bearing()  #through each loop, these four functions need to be run that will find current bearing, interpret which key has been pressed, and compare current to set bearing
            self.key_tracker()
            self.interpret_keys()
            self.diff_checker()

    def compass_bearing(self):
        #finds the current bearing and writes a text file for text to speech conversion
        if time.time() - self.t0 > 1:   #if 1 second has passed
                bearing_data = compass.find_bearing()   #run calibrated compass function that finds bearing
                self.current_bearing = bearing_data[1]
        with open('/home/pi/summer2015/Keypad/bearing.txt', 'w') as f:
            f.write(bearing_data[0])
            self.t0 = time.time()   #resets t0 to check if another 1 second has passed
    
    def key_tracker(self):
    #performs a digitalRead on the output of the MCP23017 and appends to a list the sequence of pressed keys
        key_presses = []    #list used in this function that will contain 1s and 0s depending on what keys have been pressed
        for i in range(65, 77):     #reads the digital output of all the MCP23017 pins with 
            R_val = wiringpi.digitalRead(i)
            key_presses.append(dR_val)
    
        for j in range(len(key_presses)):   #reads the 1s and 0s and determines which binary digit corresponds to which key 
                if key_presses[j]:  #if the key is a 1, evalutes to True
                    self.seq.append(self.key_val[j])    #find the corresponding value of the key
                    time.sleep(0.2) #sleep tuned to record every key press but not double count when a key is pressed
    
    def interpret_keys(self):
    #performs an action depending on which key has been pressed or the sequence of keys that have been pressed
        for key in range(len(self.seq)):
            if self.seq[key] == '1 key':    #if the 1 key is pressed, we say the current bearing and set it as the set bearing
                os.system('flite -voice slt /home/pi/summer2015/Audio/bearing.wav "$(cat /home/pi/summer2015/Keypad/bearing.txt)"') #text to speech conversion
                os.system('aplay /home/pi/summer2015/Audio/bearing.wav')
                self.set_set_bearing = True #now that we have a set bearing, we need to check to see if the current bearing differs from the set bearing in diff_checker
                self.set_bearing = self.current_bearing
                del self.seq[key]   #we delete the key once we perform the relevant actions so that we don't repeat those actions
            elif self.seq[key] == '2 key':  #if the 2 key is pressed, we just say the current bearing
                os.system('flite -voice slt /home/pi/summer2015/Audio/bearing.wav "$(cat /home/pi/summer2015/Keypad/bearing.txt)"')
                os.system('aplay /home/pi/summer2015/Audio/bearing.wav')
                del self.seq[key]
            elif self.seq[key] == '3 key': # produces the current water speed reading
                os.system('flite -voice slt /home/pi/summer2015/Audio/WaterSpeed.wav "$(cat /home/pi/summer2015/Data/WaterData.txt)"')
                os.syatem('aplay /home/pi/summer2015/Audio/WaterSpeed.wav')
                del self.seq[key]
            elif self.seq[key] == '4 key': # produces the current wind speed reading
                os.system('flite -voice slt /home/pi/summer2015/Audio/WindSpeed.wav "(cat /home/pi/summer2015/Data/WindData.txt)"')
                os.system('aplay /home/pi/summer2015/Audio/WindSpeed.wav')
                del self.seq[key]
            elif self.seq[key] == '5 key': # produces the current wind direction
                os.system ('flite -voice slt /home/pi/summer2015/Audio/WindDirection.wav "$(cat /home/pi/summer2015/Data/WindDirection.txt)"')
                os.system('aplay /home/pi/summer2015/Audio/WindDirection.wav')
                del self.seq[key]
            elif self.seq[key] == '6 key':
                del self.seq[key]
            elif self.seq[key] == '7 key':
                del self.seq[key]

    def diff_checker(self):
    #checks to see if current bearing differs from the set bearing by greater than 20 degrees and automatically tells the user on what side they are off from their set bearing and by how much
        if self.set_set_bearing:    #only runs if a set bearing has been set
            if self.current_bearing - self.set_bearing > 20 and time.time() - self.t1 > 10:
                diff = int(round(self.current_bearing - self.set_bearing, -1))
                with open('/home/pi/summer2015/Keypad/diff.txt', 'w') as g:
                    if abs(diff) > 180:     #our solution to doing the modular math of 0/360 degrees for the compass is to essentially say that off starboard 340 = off port 20
                        g.write('Off starboard ' + str(diff))
                    else:
                        g.write('Off port ' + str(diff))
                    os.system('flite -voice slt /home/pi/summer2015/Keypad/diff.wav "$(cat /home/pi/summer2015/Keypad/diff.txt)"')  #text to speech conversion for the difference between current and set bearing and on what side
                    os.system('aplay /home/pi/summer2015/Keypad/diff.wav')
                    self.t1 = time.time()
        elif self.current_bearing - self.set_bearing < -20 and time.time() - self.t1 > 10:
            diff = int(round(self.set_bearing - self.current_bearing, -1))
            with open('/home/pi/summer2015/Keypad/diff.txt', 'w') as g:
                if abs(diff) > 180:
                    g.write('Off port ' + str(diff))
                else:
                    g.write('Off starboard ' + str(diff))
                os.system('flite -voice slt /home/pi/summer2015/Keypad/diff.wav "$(cat /home/pi/summer2015/Keypad/diff.txt)"')
                os.system('aplay /home/pi/summer2015/Keypad/diff.wav')
                self.t1 = time.time() 
        else:
            pass

# def keypad_entry():
# #So the purpose of this function is to keep track of the blind sailor's actions as they press keys on the keypad. It takes no input.
# #The output is the text to speech conversion depending on their key press. Right now, we have that when the 2 key on the keypad is pressed
# #we perform a text to speech conversion with the current bearing and we tell the blind sailor their current bearing. When the 1 key is
# #pressed, we say the current bearing and we set that bearing as the set bearing. Now when the boat deviates from that set bearing by greater
# #than 20 degrees on either port or starboard, we perform a text to speech conversion that tells them on what side they are off and by how
# #many degrees, rounded to the 10s.

#     seq = []    #empty list that keeps track of the sequence of keys that have been pressed
#     set_set_bearing = False #the 1 key has not been pressed so there is no set bearing that has been set, Jacob gave me the variable name so blame him
#     t0 = time.time()    #use this time to check if 1 second has been passed to take a new bearing measurement
#     t1 = time.time()    #use this time to check is 10 seconds have passed to report how off set bearing the boat is
#     while True:     
#         key_presses = []    #so the list that contains the 1s and 0s that are the digitalRead output of the MCP23017 is initialized as an empty list and each time through the loop, emptied
#     if time.time() - t0 > 1:    #if 1 second has passed, read the current bearing from the compass
#         bearing_data = compass.find_bearing()
       
#         #this is where code would go to write to a blackbox somewhere using the XBees or bluetooth or something, use bearing_data[0] for string, bearing_data[1] for just bearing value and time.time() to timestamp data
     
#         with open('/home/pi/Sailing_Team/Keypad/bearing.txt', 'w') as f:    #write this output to a bearing.txt file for the text to speech conversion
#             f.write(bearing_data[0])
       
#         t0 = time.time()    #resets t0 so that we wait until 1 more second has passed before reading compass bearing

#         for i in range(65, 77): #performs a digitalRead on MCP23017 pins to see which keys have been pressed, append those values to key press
#         dR_val = wiringpi.digitalRead(i)
#         key_presses.append(dR_val)

#         for j in range(len(key_presses)):   #key_presses now contains a list of 1s and 0s where the 1s correspond to the buttons that have been pressed
#         if key_presses[j]:      #if a key has been pressed, we use the key_val list above to relate each 1 to the relevant key
#             seq.append(key_val[j])
#             time.sleep(0.2) #sleep is tuned so that pressing a button won't accidentally account for multiple entries in sequence list but still captures all keys pressed
        
#     #print seq

#         for key in range(len(seq)): #seq is a list that contains the sequence of keys that have been pressed, for each key, we perform a certain action
#         if seq[key] == '1 key':
#         os.system('pico2wave -w /home/pi/Sailing_Team/Keypad/bearing.wav "$(cat /home/pi/Sailing_Team/Keypad/bearing.txt)"') #creates a speech file called bearing.wav that reads from the bearing.txt file and performs text to speech conversion
#         os.system("aplay /home/pi/Sailing_Team/Keypad/bearing.wav")     #says the current bearing
#         set_bearing = bearing_data[1] #sets the current bearing as the set bearing
#         #print set_bearing
#         set_set_bearing = True  #now that we have a set bearing, we have to check if the boat goes off course
#         del seq[key]    #we delete the key from seq so that this action isn't performed again unless the key is pressed again

#         elif seq[key] == '2 key':
#             os.system('pico2wave -w /home/pi/Sailing_Team/Keypad/bearing.wav "$(cat /home/pi/Sailing_Team/Keypad/bearing.txt)"')
#         os.system("aplay /home/pi/Sailing_Team/Keypad/bearing.wav") #only says the current bearing
#             del seq[key]
    
#     if set_set_bearing:
#         #print bearing_data[1]
        
#         if bearing_data[1] - set_bearing > 20 and time.time() - t1 > 10: #checks if 10 seconds have passed and the difference ebtween set bearing and current bearing is greater than 20 degrees
#         diff = int(round(bearing_data[1] - set_bearing, -1))    #finds the difference between the set bearing and the current bearing and rounds it to the nearest 10th
        
#         with open('/home/pi/Sailing_Team/Keypad/diff.txt', 'w') as g:   #write the difference to a text file for text to speech conversion
#             if abs(diff) > 180: #kind of jank but off 340 starboard is also the same as off 20 port, this is our solution to the whole 360 to 0 degrees problem
#             g.write('Off starboard ' + str(360 - diff))
#             else:
#                 g.write('Off port ' + str(diff))    #so we write to a text file with the direction the boat is off by and the degrees rounded to the 10s
#         os.system('pico2wave -w /home/pi/Sailing_Team/Keypad/off_set_bearing.wav "$(cat /home/pi/Sailing_Team/Keypad/diff.txt)"')
#         os.system("aplay /home/pi/Sailing_Team/Keypad/off_set_bearing.wav") #perform text to speech conversion with pico2wave and play the relevant .wav file
#         t1 = time.time()
#         elif bearing_data[1] - set_bearing < -20 and time.time() - t1 > 10:
#         diff = int(round(set_bearing - bearing_data[1], -1))
#         with open('/home/pi/Sailing_Team/Keypad/diff.txt', 'w') as g:
#             if abs(diff) > 180:
#             g.write('Off port ' + str(360 - diff))
#             else:
#                 g.write('Off starboard ' + str(diff))
#         os.system('pico2wave -w /home/pi/Sailing_Team/Keypad/off_set_bearing.wav "$(cat /home/pi/Sailing_Team/Keypad/diff.txt)"')
#         os.system("aplay /home/pi/Sailing_Team/Keypad/off_set_bearing.wav")
#         t1 = time.time()
#     else:
#         pass


#if __name__ == '__main__':
    #keypad_entry()
Keypad()
