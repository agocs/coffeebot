#!/usr/bin/env python
import datetime
import time
import serial

class coffeepi_serial_lcd:
	def __init__(self, port, speed, program="Coffeebot 3000"):
		self.port = port
		self.speed = speed
		self.program = program
		self.lcd = serial.Serial(port=self.port, baudrate=self.speed)

		if self.lcd.isOpen():
			self.lcd.write(chr(32) * 32)
			self.lcd.write(chr(17))
			self.lcd.write(chr(12))
			time.sleep(5)
			self.lcd.write(chr(22))

			self.lcd.write(chr(128))
			self.lcd.write(self.program)
			self.lcd.write(chr(148))

	def formatPercent(self, level, side):
		if level == 0:
			fl = 1
		elif level == 1:
			fl = 3
		else:
			fl = 2

		fstr = str(level*100)[:fl] + '%'
		pad = chr(32) * (5 - len(fstr))

		if side == "left":
			fstr = pad + fstr

		if side == "right":
			fstr = fstr + pad

		if level == 0:
			fstr = "EMPTY"

		return fstr

	def writeToLcd(self, data):
		#message += chr(32) * (16 - len(message))
		#message format will be as follows:
		# LINE1: <-00:00||00:00->		*NOTE: IF timespan > 24 hours 00:00 = OLD!!
		# LINE2:    000%||000%
		now = time.time()

		pot1 = data[0]
		p1last = pot1["lastBrew"]
		p1delta = now - p1last
		m1, s1 = divmod(p1delta, 60)
		h1, m1 = divmod(m1, 60)

		if h1 > 24:
			p1age = " OLD "
		else:
			p1age = "%02d:%02d" % (h1, m1)

		p1level = self.formatPercent(pot1["currentLevel"], "left")

		if p1level == "EMPTY":
			p1age = "EMPTY"

		pot2 = data[1]
		p2last = pot2["lastBrew"]
		p2delta = now - p2last
		m2, s2 = divmod(p2delta, 60)
		h2, m2 = divmod(m2, 60)

		if h2 > 24:
			p2age = " OLD "
		else:
			p2age = "%02d:%02d" % (h2, m2)

		p2level = self.formatPercent(pot2["currentLevel"], "right")

		if p2level == "EMPTY":
			p2age = "EMPTY"

		message = "<-" + p1age + "||" + p2age + "->"
		##message += "  " + p1level + "||" + p2level + "  "
		message += "COFFEE BOT 3000"
		self.lcd.write(chr(128))
		self.lcd.write(message)

