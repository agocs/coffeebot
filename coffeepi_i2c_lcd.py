#!/usr/bin/env python
import time
import smbus

# This is a controller for displaying data on an LCD via I2C

# THIS ADDRESS WILL PROBABLY BE WRONG AND NEEDS TO BE CHANGED; USE I2CDETECT TO GET THIS DETAIL
bus = smbus.SMBus(0)
address = 0x60

class I2C_LCD:
	def __init__(self)