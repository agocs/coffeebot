import unittest
import sys
import time

sys.path.append("../../")

from coffee_pot import coffee_pot



class TestWriteLastBrew(unittest.TestCase):
    def setUp(self):
        self.test_coffee_pot = coffee_pot("test", 
                    full=70, 
                    empty=35, 
                    off=20, 
                    max=125, 
                    file="coffe_pot_test.txt")

    def test_write(self):
        self.test_coffee_pot.write_last_brew()
        last_brew = open(self.test_coffee_pot.file, "r").readline()
        self.assertAlmostEqual(int(time.time()), int(float(last_brew)))

if __name__ == '__main__':
    unittest.main()
