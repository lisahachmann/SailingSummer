#PiServer, for the Cabin's Pi to listen to the Keypad

import CN_Sockets #so you can use CNTRL-C to interrupt and break the script
import os
import sys
class UDP_RX(object):
    """This code was mostly taken from the CompNet Lab 4, under Alex Morrow at Olin College of Engineering. It originally demonstrated how to receive a
message from a client by acting as a server and using UDP communication protocols and sockets. It was modified to meet Team Sailing's needs to make
a navigational system for blind sailors- in particular to transmit keypad presses to a cabin raspberry Pi to then have audio output"""

    def __init__(self,IP="192.168.17.142",port=6076):
        bytedict = {'/x00':0, '/x01':1}
        commanddict = {'100000000000':self.sayhi, '01000000000':self.sayhi, '001000000000':self.water_speed,
                        '000100000000':self.wind_speed,'000010000000':self.sayhi, '000001000000':self.sayhi,
                        '000000100000':self.sayhi,'000000010000':self.sayhi, '000000001000':self.sayhi,
                        '000000000100':self.sayhi,'000000000010': self.sayhi, '000000000001':self.sayhi}
        socket, AF_INET, SOCK_DGRAM, timeout = CN_Sockets.socket, CN_Sockets.AF_INET, CN_Sockets.SOCK_DGRAM, CN_Sockets.timeout
        #                                      the socket class    the IPv4 address model    The UDP layer 4 protocol    The event name for a socket timout
        lmessage = []
#        self.sayhi()
        sock= socket(AF_INET, SOCK_DGRAM)
        sock.bind((IP,port))  # bind sets up a relationship in the linux kernel between the process running UCP_RX and the port number                                   
        sock.settimeout(2.0) # create a 2 second timeout so that we can use ctrl-c to stop a blocked server if the client doesn't work.          
        print ("UDP Server started on IP Address {}, port {}".format(IP,port))
        while True:
            try:
                bytearray_msg, source_address = sock.recvfrom(1024) # 1024 is the buffer length allocated for receiving the datagram (i.e., the packet)
                print source_address                                          
                tup = tuple(bytearray_msg)
                for t in tup:
                    lmessage.append(self.B2i(t))
                keycommand = "".join(lmessage)
                print keycommand
                commanddict[keycommand]()
                lmessage = []
                keycommand = ""
                print keycommand
                source_IP, source_port = source_address    # the source iaddress is (server IP address,client port number)
                # where client port number is allocated to the TX process by the Linux kernel as part of the TX network stack))          
                print "\nMessage received from ip address {}, port {}:".format(source_IP,source_port) #so you can see it working
            except timeout:        
            #prints a rows of dots so you can see it working/waiting 
                print "."
                continue  # go wait again
    def B2i(self,byte):
        if byte == '\x00':
            return '0'
        else: 
            return '1'
    def sayhi(self):
        print "it routed right"
        os.system('aplay /home/pi/summer2015/testing.wav')
        return 
    def say_bearing(self):
        pass
    def set_bearing(self):
        pass
    def water_speed(self):
        os.system('text2wave /home/pi/summer2015/Audio/WaterSpeed.txt -o WaterSpeed.wav')
        os.system('aplay WaterSpeed.wav')
    def wind_speed(self):
        os.system('text2wave /home/pi/summer2015/Audio/WindSpeed.txt -o WindSpeed.wav')
        os.system('aplay WindSpeed.wav')
    def wind_direction(self):
        os.system('text2wave /home/pi/summer2015/Audio/WindDirection.txt -o WindDirection.wav')
        os.system('aplay WindSpeed.wav')

if __name__ == "__main__":
    UDP_RX()