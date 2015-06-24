#!/usr/bin/python
import serial, time
from struct import pack

"""
Connects to a SkyTraq Venus on ttyUSB0 and sends some configuration commands

TODO: 
- Verify device has booted after each configuration command has been sent
- Confirm setting with appropriate read command and parse response
- Decide how to actually configure things


Things we definitely want to configure:
    Navigation mode = Airborn
    Bitrate = 115200
    Binary mode (maybe?)
    Update rate = 20 Hz
    Disable SAEE

Venus 8 ROM versions:
    Kernel Version 2.0.2
    Software Version 1.8.27
    Revision 2013.2.21
"""

ser = serial.Serial('/dev/ttyUSB0')

def send_command(data):
    ser.flushInput()
    ser.write(format_data(data))
    time.sleep(.1)
    return ser.read(100)

def format_data(data):
    check = 0
    string = pack(">HH", 0xA0A1, len(data))
    for byte in data:
        check ^= byte
        string += pack("B", byte)
    string += pack(">BH", check, 0x0D0A)
    return string


ser.baudrate=9600
send_command([0x05, 0x00, 0x05, 1])	# set baud 115200
time.sleep(.1)
ser.baudrate=115200
time.sleep(.1)
send_command([0x64, 0x17, 5, 1])	# Navigation mode = airborne
send_command([0x63, 0x01, 0, 1])	# Disable SAEE
print send_command([0x0E, 20, 1])[30:]	# 20Hz
