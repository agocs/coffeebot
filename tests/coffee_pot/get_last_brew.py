import unittest
import sys
import time
import os

sys.path.append("../../")

from coffee_pot import coffee_pot

class TestGetLastBrew(unittest.TestCase):
    def setUp(self):
        self.test_coffee_pot = coffee_pot("test", 
                    full=70, 
                    empty=35, 
                    off=20, 
                    max=125, 
                    file="coffee_pot_test.txt")


    def test_tests(self):
        self.assertTrue(True)

    def test_last_brew_nofile(self):
        if os.path.exists("./" + self.test_coffee_pot.file):
        	os.remove("./" + self.test_coffee_pot.file)
        self.assertTrue(time.time() - 1 < self.test_coffee_pot.get_last_brew() and time.time() + 1 > self.test_coffee_pot.get_last_brew())

    def test_lest_brew_file(self):
        last_brew = open(self.test_coffee_pot.file, 'w+')
        last_brew.write(str(time.time()-500))
        last_brew.close()
        self.assertEqual(int(float(self.test_coffee_pot.get_last_brew())), int(time.time() - 500))




if __name__ == '__main__':
	unittest.main()
