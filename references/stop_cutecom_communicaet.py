#!/usr/bin/env python
#coding=utf-8

import serial
import struct
import time

if __name__ == '__main__':
    print('serial')
    ser = serial.Serial('/dev/carserial','9600')
    if ser.is_open:
        print('open_success')
    time.sleep(2)
    ser.write(b'\x41\x54\x06\x20\x00\x00\x08\x01\x01\x04\x00\x01\x00\x00\x00\x0d\x0a')
    print('success')
    time.sleep(1)

