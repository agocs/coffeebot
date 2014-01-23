#!/usr/bin/env python
from datetime import datetime, date, time
import serial


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
			#time.sleep(5)
			self.lcd.write(chr(22))
			
			self.lcd.write(chr(128))
			self.lcd.write(self.program)
			self.lcd.write(chr(148))

	def writeToLcd(self, data):
		#message += chr(32) * (16 - len(message))
		#message format will be as follows:
		# LINE1: <-00:00||00:00->		*NOTE: IF timespan > 24 hours 00:00 = OLD!!
		# LINE2:    000%||000%	
		now = datetime.now()

		#p1last = data[0]["lastBrew"]
		d1 = date(2014, 1, 22)
		t1 = time(21, 15)
		p1last = datetime.combine(d1, t1)
		p1delta = now - p1last
		m1, s1 = divmod(int(p1delta), 60)
		h1, m1 = divmod(m1, 60)

		#p2last = data[1]["lastBrew"]
		d2 = date(2014, 1, 22)
		t2 = time(12, 35)
		p2last = datetime.combine(d2, t2)
		p2delta = now - p2last
		m2, s2 = divmod(int(p2delta), 60)
		h2, m2 = divmod(m2, 60)

		p1string = "%02d:%02d" % (h1, m1)
		p2string = "%02d:%02d" % (h2, m2)

		p1level = str(0.54*100)[:4] + '%'
		p2level = str(0.77*100)[:4] + '%'

		message = "<-" + p1string + "||" + p2string + "->"
		message += "  " + p1level + "||" + p2level + "  "

		self.lcd.write(chr(128))
		self.lcd.write(message)
