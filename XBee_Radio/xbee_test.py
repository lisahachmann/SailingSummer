import serial

ser = serial.Serial('/dev/ttyUSB0', 9600)
string = 'Hello from Raspberry Pi'
print 'Sending "%s"' % string
ser.write('%s\n' % string)

while True:
    incoming = ser.readline().strip()
    print 'Recieved %s' % incoming
    ser.write('RPi Recieved: %s\n' % incoming)
