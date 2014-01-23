#!/usr/bin/env python
import adafruit_lcdbackpack

# This is a controller for displaying data on an LCD via I2C


class I2C_LCD:
	def __init__(self, bus, address):
		initLcd(self, bus, address)

	def initLcd(self, bus, address):
		self.lcd = Adafruit_CharLCDBackpack(bus, address, false)
		self.lcd.begin(16,2)
		self.lcd.clear()
		self.lcd.display()



	def writeLcd(self, message):
		self.lcd.message(message)
