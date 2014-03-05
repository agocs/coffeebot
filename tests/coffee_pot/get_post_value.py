import unittest
import sys
import time

sys.path.append("../../")

from coffee_pot import coffee_pot



class TestGetPostValue(unittest.TestCase):
    def setUp(self):
        self.test_coffee_pot = coffee_pot("test", 
                    full=1, 
                    empty=0, 
                    off=0, 
                    max=1, 
                    file="coffe_pot_test.txt")	
        self.test_coffee_pot.values = [.5, 1, .5, 1, .5, 1, .5, 1, .5, 1]

    def test_average(self):
        self.assertEqual(.75, self.test_coffee_pot.get_post_value())

if __name__ == '__main__':
	unittest.main()
