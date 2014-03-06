import unittest
import sys
import time

sys.path.append("../../")

from coffeepi_controller import *



class TestInitializeCoffeePots(unittest.TestCase):
    def setUp(self):
        initialize_coffee_pots()
    	
    def test_full_empty_against_max(self):
       self.assertTrue(COFFEE_POTS["1"].full <= VALID_DATA_MAX and COFFEE_POTS["2"].empty >= VALID_DATA_MIN)

    def test_dict_size(self):
    	self.assertEqual(len(COFFEE_POTS), 2)



if __name__ == '__main__':
	unittest.main()