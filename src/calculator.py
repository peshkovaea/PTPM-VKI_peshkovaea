class TriangleCalculator:
    def determine_type(self, a: float, b: float, c: float) -> tuple[str, str]:
        """Возвращает (тип_треугольника, сообщение_об_ошибке)."""
        if a <= 0 or b <= 0 or c <= 0:
            return "", "Стороны должны быть положительными"
        if a + b <= c or a + c <= b or b + c <= a:
            return "", "Треугольник не существует"
        if a == b == c:
            return "равносторонний", ""
        if a == b or b == c or a == c:
            return "равнобедренный", ""
        return "разносторонний", ""

