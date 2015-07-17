"""ClientKeypad, for transmitting key presses to the Pi in the cabin, the PiCabinServer. This code was 
mostly taken from the CompNet Lab 4, under Alex Morrow at Olin College of Engineering. It originally demonstrated how to send a message 
by acting as a client to a server and using UDP communication protocols and sockets. It was modified to meet Team Sailing's needs to make
a navigational system for blind sailors- in particular to transmit keypad presses to a cabin raspberry Pi to then have audio output. 
The keypad input uses Edge detection (rising/falling detection) before sending the information to the other Pi with sockets, to then play audio"""

import CN_Sockets # CN_Sockets adds ability to interrupt "while True" loop with ctl-C
import RPi.GPIO as GPIO  
from time import sleep  
import Queue
import threading 
import time

class TX_Keypad(object):
    def __init__(self,Server_Address=("192.168.17.142",6076)):  
    # create a socket instance, with the "address" is IPv4 address ("127.0.0.1") and port number (5280)
    #use 127.0.0.1 if you want to communicate within a single machine (laptop or Pi
        self.seq = Queue.Queue() #start a queue
      #  GPIO.setmode(GPIO.BCM) # set up BCM GPIO numbering system     
    #reference
        self.Server_Address = Server_Address
        self.pindict = {12:0, 25:1, 24:2, 22:3, 5:4, 6:5, 13:6, 19:7, 26:8, 21:9, 20:10, 16:11}
        self.gpioinputs = [4,17, 27,22, 5, 6, 13, 19, 26, 21, 20, 16]
        self.keypin = ['*','7','4','1', '0', '8', '5', '2', '#', '9', '6', '3']
        self.key_state = 12*[0]
        self.down_keys = 0
        # socket = CN_sockets.socket, which is socket.socket with a slignt modification to allow you to use ctl-c to terminate a test safely
        # CN_sockets.AF_INET is the constant 2, indicating that the address is in IPv4 format
        # CN_sockets.SOCK_DGRAM is the constant 2, indicating that the programmer intends to use the Universal Datagram Protocol of the Transport Layer
        socket, AF_INET, SOCK_DGRAM = CN_Sockets.socket, CN_Sockets.AF_INET, CN_Sockets.SOCK_DGRAM
        self.sock= socket(AF_INET,SOCK_DGRAM)  # open the socket
        print "UDP_TX client started for UDP_Server at IP address {} on port {}".format(Server_Address[0],Server_Address[1])

    def my_callback(self,gpiopin):
        #global key_state, keypin, inputs, down_keys
        #pin = keypin.index(gpiopin)
        if GPIO.input(gpiopin): #if it's high, mention it in the key_state list
            self.key_state[self.pindict[gpiopin]] = 1
            self.down_keys +=1
        else:
            self.down_keys -=1
            if self.down_keys == 0:
                print self.key_state
                if any( self.key_state):
                    self.seq.put(self.key_state)
                    self.key_state = 12 * [0]
                    return 
        return self.key_state

    def __call__(self):
#        GPIO.setmode(GPIO.BCM)
        while True:
            GPIO.setmode(GPIO.BCM)
            for pin in self.gpioinputs:
                GPIO.setup(pin, GPIO.IN) 
                GPIO.add_event_detect(pin, GPIO.BOTH, callback=self.my_callback, bouncetime = 10)
            # str_message = input("Enter message to send to server:\n") #means you need quotation marks around your message
            # if not str_message: # an return with no characters terminates the loop
            #     break
            if self.seq:
                bytearray_message = bytearray(self.seq.get()) 
        # note that sockets can only send 8-bit bytes. Since Python uses the Unicode character set, we have to specify 
        #this to convert the message typed in by the user (str_message) to 8-bit ascii 
            bytes_sent = self.sock.sendto(bytearray_message, self.Server_Address) # this is the command to send the bytes in bytearray to the server at "Server_Address"
            print "{} bytes sent".format(bytes_sent) #sock_sendto returns number of bytes send.
            try:
                print "Began program"  
      #          bytearray_msg, Server_Address = sock.recvfrom(1024) # 1024 is the buffer length allocated for receiving the datagram (i.e., the packet)        
                server_IP, server_port = Server_Address    
                # the source iaddress is (IP,client port number)
                # where client port number is allocated to the TX process by the Linux kernel as part of the TX network stack))            
                print "\nMessage received from ip address {}, port {}:".format(server_IP,server_port)
                decoded = (bytearray_msg.decode("UTF-8"))
                print (decoded) # print the message sent by the user of the  UDP_TX module.
            except:
                    pass
            finally:
                GPIO.cleanup()

        # # Define a threaded callback function to run in another thread when events are detected  

print("UDP_Client ended")

if __name__ == "__main__":
    KeyLime = TX_Keypad()
    KeyLime()
