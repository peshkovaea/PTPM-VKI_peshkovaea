import math
import logging
import sys

# Шаблон строки лога (аналог template в Serilog)
# Содержит: время, уровень (до 7 символов для выравнивания), имя логгера и сообщение
log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

# Базовая настройка корневого логгера
logging.basicConfig(
    level=logging.DEBUG, # Минимальный уровень логирования (аналог MinimumLevel.Debug)
    format=log_format,
    datefmt=date_format,
    handlers=[
        logging.StreamHandler(sys.stdout),          # Настройка логирования в консоль
        logging.FileHandler("logs/file_txt.log", encoding="utf-8") # Настройка логирования в файл
    ]
)

logging.info("Логгер успешно сконфигурирован")
logging.info("Приложение запущено")

def parse_side(s):
    #преобразуем строку в положительное float, если нет то None
    try:
        value = float(s)
    except ValueError:
        return None
    if value <= 0:
        return None
    return value


def classify(a, b, c):
    #определяем тип треугольника
    if a + b <= c or a + c <= b or b + c <= a:
        return "не треугольник"
    if a == b == c:
        return "равносторонний"
    if a == b or b == c or a == c:
        return "равнобедренный"
    return "разносторонний"


def calc_vertices(a, b, c):
    #вычисляем координаты трёх вершин, вписывая треугольник в поле 100x100
    # Вершина A в (0,0), вершина B на оси X
    x1, y1 = 0.0, 0.0
    x2, y2 = c, 0.0

    # Координаты вершины C по теореме косинусов
    cos_a = (c * c + a * a - b * b) / (2 * c * a)
    cos_a = max(-1.0, min(1.0, cos_a))  # защита от погрешностей float
    sin_a = math.sqrt(1 - cos_a * cos_a)

    x3 = a * cos_a
    y3 = a * sin_a

    # Находим границы треугольника
    min_x = min(x1, x2, x3)
    max_x = max(x1, x2, x3)
    min_y = min(y1, y2, y3)
    max_y = max(y1, y2, y3)

    width = max_x - min_x
    height = max_y - min_y

    # масштаб для вписывания в 100x100 с отступом 5 px
    margin = 5
    free = 100 - 2 * margin
    if width > 0 and height > 0:
        scale = min(free / width, free / height)
    elif width > 0:
        scale = free / width
    elif height > 0:
        scale = free / height
    else:
        scale = 1.0

    def to_screen(x, y):
        nx = (x - min_x) * scale + margin
        ny = (y - min_y) * scale + margin
        # инвертируем Y 
        return (int(round(nx)), int(round(100 - ny)))

    return [to_screen(x1, y1), to_screen(x2, y2), to_screen(x3, y3)]


def main():
    lines = []
    for _ in range(3):
        try:
            lines.append(input())
        except EOFError:
            lines.append("")

    sides = [parse_side(s) for s in lines]

    # Если хотя бы одна строка нечисловая или <= 0
    if any(s is None for s in sides):
        print("")
        print([(-2, -2), (-2, -2), (-2, -2)])
        return

    a, b, c = sides
    tri_type = classify(a, b, c)
    print(tri_type)

    if tri_type == "не треугольник":
        print([(-1, -1), (-1, -1), (-1, -1)])
    else:
        print(calc_vertices(a, b, c))


if __name__ == "__main__":
    main()