import unittest
from src.calculator import TriangleCalculator


class TestTriangleCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = TriangleCalculator()

    def test_equilateral(self):
        t_type, err = self.calc.determine_type(3, 3, 3)
        self.assertEqual(t_type, "равносторонний")
        self.assertEqual(err, "")

    def test_isosceles(self):
        t_type, err = self.calc.determine_type(3, 3, 4)
        self.assertEqual(t_type, "равнобедренный")
        self.assertEqual(err, "")

    def test_scalene(self):
        t_type, err = self.calc.determine_type(3, 4, 5)
        self.assertEqual(t_type, "разносторонний")
        self.assertEqual(err, "")

    def test_invalid_negative_side(self):
        t_type, err = self.calc.determine_type(-1, 4, 5)
        self.assertEqual(t_type, "")
        self.assertIn("положительн", err.lower())

    def test_triangle_inequality_violated(self):
        t_type, err = self.calc.determine_type(1, 2, 5)
        self.assertEqual(t_type, "")
        self.assertIn("не существует", err.lower())


if __name__ == "__main__":
    unittest.main()