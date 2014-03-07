import unittest
import sys

sys.path.append("./coffee_pot")
sys.path.append("./coffeepi_controller")
sys.path.append("../")

from coffee_pot_test_suite import *
from coffeepi_controller_test_suite import *



if __name__ == '__main__':
	unittest.main()
	