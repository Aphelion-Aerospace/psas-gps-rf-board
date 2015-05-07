#!/usr/bin/python
import serial, time

"""
Connects to a SkyTraq Venus on ttyUSB0 and sends some configuration commands

TODO: 
- Verify device has booted after each configuration command has been sent
- Confirm setting with appropriate read command and parse response
- Decide how to actually configure things
"""

ser = serial.Serial('/dev/ttyUSB0')

def send_command(cmd):
    ser.flushInput()
    ser.write(cmd)
    time.sleep(.1)
    return ser.read(100)

ser.baudrate=9600
ser.write('\xA0\xA1\x00\x04\x05\x00\x05\x01\x01\x0D\x0A')	# set baud 115200
time.sleep(.1)
ser.baudrate=115200
time.sleep(.1)
send_command('\xA0\xA1\x00\x09\x08\x01\x01\x00\x00\x01\x00\x00\x01\x08\x0D\x0A')	# select GGA GSA RMC messages
send_command('\xA0\xA1\x00\x03\x37\x01\x01\x37\x0D\x0A')	# enable WAAS
send_command('\xA0\xA1\x00\x03\x3C\x00\x01\x3D\x0D\x0A')	# nav mode = Car
print send_command('\xA0\xA1\x00\x03\x0E\x0A\x01\x05\x0D\x0A')[30:]	# 10Hz
