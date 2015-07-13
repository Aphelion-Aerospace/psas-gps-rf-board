#!/usr/bin/python
import serial, time
from struct import pack
import sys

"""
Connects to a SkyTraq Venus on ttyUSB0 and sends some configuration commands

TODO: 
- Verify device has booted after each configuration command has been sent
- Confirm setting with appropriate read command and parse response
- Decide how to actually configure things


Things we definitely want to configure:
    Navigation mode = Airborn
    Bitrate = 115200
    Binary mode
    Update rate = 20 Hz
    Disable SAEE

Venus 8 ROM versions:
    Kernel Version 2.1.5
    ODM Version 1.7.27
    Revision 2015.1.27
"""

ser = serial.Serial('/dev/ttyUSB0', timeout=0.1)

def send_command(data):
    ser.flushInput()
    ser.write(format_data(data))
    time.sleep(.1)
    response = ser.read(100)
    print ' '.join('{:02X}'.format(ord(b)) for b in response)

def format_data(data):
    check = 0
    string = pack(">HH", 0xA0A1, len(data))
    for byte in data:
        check ^= byte
        string += pack("B", byte)
    string += pack(">BH", check, 0x0D0A)
    return string

def baud_rate(code):
    return [4800, 9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600][code]

def meas_data_rate(code):
    """Update rate for binary measurement data output. See SkyTraq AN0030."""
    return [1, 2, 4, 5, 10, 20][code]

max_channels = 20 # we don't expect more than this many satellites locked at once

baud_rate_code = 5 # see baud_rate()
nav_data_rate = 20 # Hz; update rate for navigation data message (see AN0028)
meas_data_rate_code = 5 # see meas_data_rate()
meas_time_enabled = 0
raw_meas_enabled = 0
sv_ch_status_enabled = 0
rcv_state_enabled = 0

bytes_per_second = nav_data_rate * 66

if meas_time_enabled:
    bytes_per_second += meas_data_rate(meas_data_rate_code) * 17

if raw_meas_enabled:
    bytes_per_second += meas_data_rate(meas_data_rate_code) * (10 + 23 * max_channels)

if sv_ch_status_enabled:
    bytes_per_second += meas_data_rate(meas_data_rate_code) * (10 + 10 * max_channels)

if rcv_state_enabled:
    # this message is always sent at 1Hz
    bytes_per_second += 88

# GPS subframe messages
bytes_per_second += 40 * max_channels / 6

print "minimum baud rate: {}".format(bytes_per_second * 10)
print "selected baud rate: {}".format(baud_rate(baud_rate_code))

if bytes_per_second * 10 > baud_rate(baud_rate_code):
    print " *** can't keep up with this config at this baud rate!"
    sys.exit(1)


#ser.baudrate = 115200
#send_command([0x05, 0x00, baud_rate_code, 1])
#time.sleep(.1)

ser.baudrate = baud_rate(baud_rate_code)
time.sleep(.1)

send_command([2, 1]) # query software versions

send_command([0x09, 0x02, 1])    # Set binary output mode
send_command([0x64, 0x17, 5, 1]) # Navigation mode = airborne
send_command([0x63, 0x01, 2, 1]) # Disable "Self-Aided Ephemeris Estimation" (see http://navspark.mybigcommerce.com/content/GNSSViewerUserGuide.pdf)
send_command([0x0E, nav_data_rate, 1])   # System position rate
send_command([0x11, 1, 1])   # Navigation data message rate divider
send_command([0x1E, meas_data_rate_code, meas_time_enabled, raw_meas_enabled, sv_ch_status_enabled, rcv_state_enabled, 0b0001, 1])       # Binary measurement data enable and rate

#send_command([0x10])
#send_command([0x1F])
