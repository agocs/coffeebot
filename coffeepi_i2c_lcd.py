#!/usr/bin/env python
from adafruit_lcdbackpack import Adafruit_CharLCDBackpack

class I2C_LCD:
	# This is a controller for displaying data on an LCD via I2C

	def __init__(self, bus, address):
		initLcd(self, bus, address)

	def initLcd(self, bus, address):
		self.lcd = Adafruit_CharLCDBackpack(bus, address, false)
		self.lcd.begin(16,2)
		self.lcd.clear()
		self.lcd.display()

	def writeLcd(self, message):
		self.lcd.message(message)
