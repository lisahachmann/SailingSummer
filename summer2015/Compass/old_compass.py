#!/usr/bin/python
import smbus
import time
import math

#Code source: http://blog.bitify.co.uk/2013/11/connecting-and-calibrating-hmc5883l.html

bus = smbus.SMBus(1)  #1 instead of 0 because of our version of the rpi
address = 0x1e


def read_byte(adr):
    """
    not even used
    """
    return bus.read_byte_data(address, adr)


def read_word(adr):
    """
    used by read_word_2c
    reads two numbers from I2C address adr
    multiplies high by 2**8 (shifting it left in binary) and adds low
    possibly undoing a two's complement
    """
   # ready = bus.read_byte_data(address, 9)
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    #print "read_word low:", low #trying to see what's going on
    #print "read_word high:", high
    #print "read_word val:", val
    return val


def read_word_2c(adr):
    """
    reads from an output register (3, 5, or 7)
    undoes two's complement
    """
    val = read_word(adr)
    if (val >= 0x8000): #checks if first bit indicates number is negative
        return -((65535 - val) + 1)
    else:
        return val


def write_byte(adr, value):
    bus.write_byte_data(address, adr, value)

write_byte(0, 0b01110000) # Set to 8 samples @ 15Hz
write_byte(1, 0b00100000) # 1.3 gain LSb / Gauss 1090 (default)
#write_byte(1, 0b11100000) # our try to make it work
write_byte(2, 0b00000000) # Continuous sampling

scale = 0.92
#scale = 1.0     #just for testing purposes

#x_offset = 0    #just for testing purposes
#y_offset = 0
x_offset = -89
y_offset = -179


def find_bearing():
    #while True:
    x_out = (read_word_2c(3) - x_offset) * scale
    z_out = read_word_2c(5) * scale
    y_out = (read_word_2c(7) - y_offset) * scale
    print x_out
    #print y_out
    #print z_out
    bearing = math.atan2(y_out, x_out)

    if (bearing < 0):
        bearing += 2 * math.pi
    print math.degrees(bearing)

    #time.sleep(1) 
    res = int(round(math.degrees(bearing)))
    return ("Bearing: " + str(res), res)

    #with open('bearing.txt', 'w') as f:
        #f.write("Bearing: " + "%.2f" % math.degrees(bearing))
        #os.system('pico2wave -w /home/pi/Sailing_Team/Compass/bearing.wav "$(cat /home/pi/Sailing_Team/Compass/bearing.txt)"')
    #time.sleep(1)


for i in range(0,10):
    time.sleep(1)
    print find_bearing()


#while True:
    #test = find_bearing()
    #print test[1]
    #time.sleep(0.5)
#print test[1]
#def text_to_speech():
    #while True:
	#os.system('pico2wave -w /home/pi/Sailing_Team/Compass/bearing.wav "$(cat /home/pi/Sailing_Team/Compass/bearing.txt)"')

#for i in range(0,500):
    #x_out = read_word_2c(3)
    #y_out = read_word_2c(5)
    #z_out = read_word_2c(7)
    
    #bearing = math.atan2(y_out, x_out)
    #if (bearing < 0):
	#bearing += 2 * math.pi
    #f.write("{} {} {} {}\n".format(x_out, y_out, (x_out * scale), (y_out * scale)))
    #time.sleep(0.1)
