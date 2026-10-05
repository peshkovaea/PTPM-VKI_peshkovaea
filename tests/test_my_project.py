import unittest
from src.triangle import parse_side, classify, calc_vertices

"""Проверка входных данных"""
class TestParseSide(unittest.TestCase):

    def test_integer_string_returns_float(self):
        """Строка с целым числом → float."""
        self.assertEqual(parse_side("5"), 5.0)

    def test_decimal_string_returns_float(self): # Строка с дробным числом = float
        self.assertEqual(parse_side("3.14"), 3.14)

    def test_zero_returns_none(self): # Ноль недопустим — сторона должна быть > 0
        self.assertIsNone(parse_side("0"))

    def test_non_numeric_string_returns_none(self): # Нечисловая строка не должна ломать программу
        self.assertIsNone(parse_side("abc"))

    """Определение типа треугольника """
class TestClassifyTriangle(unittest.TestCase):
    def test_all_sides_equal_is_equilateral(self):
        self.assertEqual(classify(3, 3, 3), "равносторонний")

    def test_two_sides_equal_is_isosceles(self):
        self.assertEqual(classify(5, 5, 6), "равнобедренный")

    def test_all_sides_different_is_scalene(self): 
        self.assertEqual(classify(3, 4, 5), "разносторонний")

    def test_violated_inequality_is_not_triangle(self):  # Сумма двух сторон меньше третьей = не треугольник
        self.assertEqual(classify(1, 1, 10), "не треугольник")

    """Расчёт координат вершин"""
class TestCalcVertices(unittest.TestCase):
    def test_returns_exactly_three_vertices(self):
        result = calc_vertices(3, 4, 5) #функция возвращает ровно 3 вершины
        self.assertEqual(len(result), 3)
    
    def test_vertices_are_integer_tuples(self):
        result = calc_vertices(3, 4, 5) # Каждая вершина — кортеж из двух int
        for x, y in result:
            self.assertIsInstance(x, int)
            self.assertIsInstance(y, int)
   
    def test_all_vertices_fit_into_100x100_field(self): 
        result = calc_vertices(3, 4, 5) # Все координаты лежат в поле 100×100 px
        for x, y in result:
            self.assertTrue(0 <= x <= 100)
            self.assertTrue(0 <= y <= 100)

    def test_equilateral_triangle_fits_field(self):
        result = calc_vertices(10, 10, 10) # Равносторонний треугольник тоже вписывается в поле
        for x, y in result:
            self.assertTrue(0 <= x <= 100 and 0 <= y <= 100)


if __name__ == "__main__":
    unittest.main()