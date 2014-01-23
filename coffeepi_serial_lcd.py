#!/usr/bin/env python
import serial
import time

class Serial_LCD:
	def __init__(self, port, speed, program):
		self.port = port
		self.speed = speed
		self.program = program

	def initLcd(self):
		self.lcd = serial.Serial(port=self.port, baudrate=self.speed)

		if self.lcd.isOpen():
			self.lcd.write(chr(32) * 32)
			self.lcd.write(chr(12))
			self.lcd.write(chr(18))
			time.sleep(1)
			self.lcd.write(chr(128))
			self.lcd.write(self.program)
			self.lcd.write(chr(148))

	def writeToLcd(self, data):
		#message += chr(32) * (16 - len(message))
		#message format will be as follows:
		# LINE1: <-00:00||00:00->		*NOTE: IF timespan > 24 hours 00:00 = OLD!!
		# LINE2:    000%||000%	

		message = "<-00:00||00:00->"
		message += "  000%||000%   "

		self.lcd.write(chr(148))
		self.lcd.write(message)
