import unittest
from calculator import calculate_calories

class TestCalculator(unittest.TestCase):
    def test_calculate_calories(self):
        self.assertEqual(calculate_calories(10, 5, 2), 10*4 + 5*4 + 2*9)

if __name__ == '__main__':
    unittest.main()