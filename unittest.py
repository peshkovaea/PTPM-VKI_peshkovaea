import unittest
from converter import Converter


class TestConverterBoundaries(unittest.TestCase):
    def test_upper_boundary_100_7_returns_1000(self):
        self.assertEqual(Converter.do(100.7), 1000)

    def test_just_below_upper_boundary(self):
        self.assertEqual(Converter.do(100.6), 100)  # (0; 100.7): int(100.6) = 100

    def test_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            Converter.do(0.0)

    def test_lower_boundary_minus_30_4(self):
        self.assertEqual(Converter.do(-30.4), -35)  # int(-30.4) = -30; -30 - 5 = -35

    def test_just_below_lower_boundary_minus_30_5(self):
        self.assertEqual(Converter.do(-30.5), -2000)


class TestConverterPositiveRange(unittest.TestCase): #(0; 100.7)

    def test_small_positive(self):
        self.assertEqual(Converter.do(0.1), 0)

    def test_positive_truncation(self):
        self.assertEqual(Converter.do(65.7), 65)

    def test_positive_integer_part(self):
        self.assertEqual(Converter.do(99.9), 99)


class TestConverterLargePositive(unittest.TestCase): #[100.7; +∞) 

    def test_large_value(self):
        self.assertEqual(Converter.do(1000.0), 1000)

    def test_far_above(self):
        self.assertEqual(Converter.do(99999.9), 1000)


class TestConverterNegativeRange(unittest.TestCase):

    def test_negative_truncation(self): # int(-94.5) = -94 
        self.assertEqual(Converter.do(-0.5), -5)

    def test_negative_small(self): # int(-1.5) = -1; -1 - 5 = -6
        self.assertEqual(Converter.do(-1.5), -6)

    def test_negative_middle(self): # int(-15.5) = -15; -15 - 5 = -20
        self.assertEqual(Converter.do(-15.5), -20)

    def test_negative_near_boundary(self): # int(-29.9) = -29; -29 - 5 = -34
        self.assertEqual(Converter.do(-29.9), -34)


class TestConverterLargeNegative(unittest.TestCase):

    def test_below_boundary(self):
        self.assertEqual(Converter.do(-31.0), -2000)

    def test_example_from_task(self): # -94.5 попадает сюда (а не в [-30.4; 0))
        self.assertEqual(Converter.do(-94.5), -2000)

    def test_very_large_negative(self):
        self.assertEqual(Converter.do(-10000.0), -2000)


class TestConverterFullCoverage(unittest.TestCase):

    def test_all_branches(self):
        self.assertEqual(Converter.do(150.0), 1000)     # >= 100.7
        self.assertEqual(Converter.do(50.5), 50)        # (0; 100.7)
        self.assertEqual(Converter.do(-10.0), -15)      # [-30.4; 0)
        self.assertEqual(Converter.do(-50.0), -2000)    # <= -30.5
        with self.assertRaises(ValueError):
            Converter.do(0.0)                            # == 0


if __name__ == "__main__":
    unittest.main()