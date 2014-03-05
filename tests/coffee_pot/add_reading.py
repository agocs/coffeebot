import unittest
import sys

sys.path.append("../../")

from coffee_pot import coffee_pot



class TestAddReading(unittest.TestCase):
    def setUp(self):
        self.test_coffee_pot = coffee_pot("test", 
                    full=70, 
                    empty=35, 
                    off=20, 
                    max=125, 
                    file="coffe_pot_test.txt")


    def test_tests(self):
        self.assertTrue(True)


    def test_single_reading(self):
        self.test_coffee_pot.add_reading(30)
        self.assertTrue(self.test_coffee_pot.values[9] == 30)

    def test_ten_readings(self):
        for i in range(0, 10):
            self.test_coffee_pot.add_reading(i)
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], self.test_coffee_pot.values)



    
if __name__ == "__main__":
    unittest.main()
