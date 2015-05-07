#!/usr/bin/python
import serial, time

"""
Tries to figure out which baud rate the SkyTraq Venus is configured for
and issues the factory reset command.
"""

device = '/dev/ttyUSB0'
ser = serial.Serial(device)
print "Scanning %s baudrates" % device
for baud in [1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200]:
    ser.baudrate=baud
    ser.flushOutput()
    ser.flushInput()
    ser.write('\xA0\xA1\x00\x02\x02\x01\x03\x0D\x0A')	# request version
    time.sleep(.2)
    if ser.inWaiting():
	read = ser.read(ser.inWaiting())
	if '\xA0\xA1' in read:
	    print "Connected to %s at %i baud" % (device, baud)
	    #print "\\x"+"\\x".join("{:02x}".format(ord(c)) for c in read)
	    ser.write('\xA0\xA1\x00\x02\x04\x01\x05\x0D\x0A')	# factory defaults and restart
	    ser.flush()
	    ser.baudrate=9600
	    ser.flushInput()
	    print "Factory reset complete."
	    print ser.read(100)[4:]
	    break
