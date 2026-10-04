
import unittest
from src.triangle import parse_side, classify_triangle, calc_vertices


class TestParseSide(unittest.TestCase):
    """Тесты парсинга входных данных (4 теста)."""

    def test_integer_string_returns_float(self):
        """Обычное целое число превращается в float."""
        self.assertEqual(parse_side("5"), 5.0)

    def test_decimal_string_returns_float(self):
        """Дробное число корректно парсится."""
        self.assertEqual(parse_side("3.14"), 3.14)

    def test_zero_returns_none(self):
        """Ноль недопустим — сторона должна быть положительной."""
        self.assertIsNone(parse_side("0"))

    def test_non_numeric_string_returns_none(self):
        """Нечисловая строка не должна ломать программу."""
        self.assertIsNone(parse_side("abc"))


class TestClassifyTriangle(unittest.TestCase):
    """Тесты определения типа треугольника (4 теста)."""

    def test_all_sides_equal_is_equilateral(self):
        """Все стороны равны → равносторонний."""
        self.assertEqual(classify_triangle(3, 3, 3), "равносторонний")

    def test_two_sides_equal_is_isosceles(self):
        """Две стороны равны → равнобедренный."""
        self.assertEqual(classify_triangle(5, 5, 6), "равнобедренный")

    def test_all_sides_different_is_scalene(self):
        """Все стороны разные → разносторонний."""
        self.assertEqual(classify_triangle(3, 4, 5), "разносторонний")

    def test_violated_inequality_is_not_triangle(self):
        """Сумма двух сторон меньше третьей → не треугольник."""
        self.assertEqual(classify_triangle(1, 1, 10), "не треугольник")


class TestCalcVertices(unittest.TestCase):
    """Тесты расчёта координат вершин (4 теста)."""

    def test_returns_exactly_three_vertices(self):
        """Функция должна вернуть ровно 3 вершины."""
        result = calc_vertices(3, 4, 5)
        self.assertEqual(len(result), 3)

    def test_vertices_are_integer_tuples(self):
        """Каждая вершина — кортеж из двух int (для отрисовки)."""
        result = calc_vertices(3, 4, 5)
        for x, y in result:
            self.assertIsInstance(x, int)
            self.assertIsInstance(y, int)

    def test_all_vertices_fit_into_100x100_field(self):
        """Все координаты должны лежать в поле 100×100 px."""
        result = calc_vertices(3, 4, 5)
        for x, y in result:
            self.assertTrue(0 <= x <= 100)
            self.assertTrue(0 <= y <= 100)

    def test_equilateral_triangle_fits_field(self):
        """Равносторонний треугольник тоже вписывается в поле."""
        result = calc_vertices(10, 10, 10)
        for x, y in result:
            self.assertTrue(0 <= x <= 100 and 0 <= y <= 100)


if __name__ == "__main__":
    unittest.main()