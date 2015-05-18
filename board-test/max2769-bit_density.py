#!/usr/bin/python
import struct
import sys

nibble_count = 0
sign_1s = 0
mag_1s = 0
i_sign_1s = 0
i_mag_1s = 0
q_sign_1s = 0
q_mag_1s = 0

def nibble_decoder(nibble):
    global nibble_count, sign_1s, mag_1s, i_sign_1s, i_mag_1s, q_sign_1s, q_mag_1s
    nibble_count += 1
    if nibble & 0b1000:
        mag_1s += 1
        i_mag_1s += 1
    if nibble & 0b0100:
        sign_1s += 1
        i_sign_1s += 1
    if nibble & 0b0010:
        mag_1s += 1
        q_mag_1s += 1
    if nibble & 0b0001:
        sign_1s += 1
        q_sign_1s += 1

with open("gpslog", "rb") as f:
    byte = f.read(1)
    while byte:
        byte = ord(byte)
        nibble_decoder(byte & 0xf)
        nibble_decoder(byte >> 4 & 0xf)
        byte = f.read(1)
        if nibble_count >= 20971520:
            print "Stopping at 10MB"
            break

print "count: %i, sign: %i, mag: %i" % (nibble_count, sign_1s, mag_1s)
print "sign: %0.3f mag: %0.3f" % (sign_1s / 1.0 / nibble_count * 50, mag_1s / 1.0 / nibble_count * 50)
print "isign: %0.3f imag: %0.3f" % (i_sign_1s / 1.0 / nibble_count * 100, i_mag_1s / 1.0 / nibble_count * 100)
print "qsign: %0.3f qmag: %0.3f" % (q_sign_1s / 1.0 / nibble_count * 100, q_mag_1s / 1.0 / nibble_count * 100)
