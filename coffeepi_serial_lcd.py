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
		self.lcd.write(chr(148))
		if data["pot"] == "1":
			message = "<-- "
		else
			message = "--> "

		message += "Brew: " + data["lastBrew"]
		self.lcd.write(message)

		#On bottom line, display current level
		self.lcd.write()
		message = "Current: " + data["currentLevel"]

		self.lcd.write(message)
