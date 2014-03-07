import unittest
import sys
import time

sys.path.append("../../")

from coffeepi_controller import *

import reading_faker as adafruit_mcp3008



class TestReadWriteSensors(unittest.TestCase):
	def setUp(self):
		initialize_coffee_pots()
	
	def test_get_any_readings(self):
		read_write_sensors()
		self.assertFalse(COFFEE_POTS["1"].values[9] == 0)

if __name__ == '__main__':
	print COFFEE_POTS
	unittest.main()