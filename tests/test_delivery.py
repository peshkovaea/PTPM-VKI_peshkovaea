import unittest
from src.Delivery import calculate_delivery_cost

"""Проверка входных данных"""
class TestValidation(unittest.TestCase):
    
    def test_weight_below_minimum_returns_error(self):
        self.assertEqual(calculate_delivery_cost(0.05, 100, "обычный"), #вес меньше 0,1 кг
                         (-1, "0000-00-00"))

    def test_distance_above_maximum_returns_error(self):
        self.assertEqual(calculate_delivery_cost(1, 5001, "обычный"), #дистанция больше 5000км
                         (-1, "0000-00-00"))

    def test_unknown_package_type_returns_error(self):
        self.assertEqual(calculate_delivery_cost(1, 100, "магический"), #неизвестный тип посылки
                         (-1, "0000-00-00"))

    """Базовая тарифная сетка"""
class TestBaseCost(unittest.TestCase):
    def test_base_cost_for_small_order(self):
        cost, _ = calculate_delivery_cost(1, 100, "обычный") # 1кг, 100км = 200 + 500 = 700
        self.assertEqual(cost, 700)

    def test_cost_scales_with_distance(self):
        cost1, _ = calculate_delivery_cost(1, 100, "обычный") # дистанция + 100 км => +500 руб.
        cost2, _ = calculate_delivery_cost(1, 200, "обычный")
        self.assertEqual(cost2 - cost1, 500)

    """Весовые коэффициенты"""
class TestWeightCoefficients(unittest.TestCase):
    def test_weight_up_to_5kg_no_surcharge(self):
        cost, _ = calculate_delivery_cost(5.0, 100, "обычный") # до 5кг без надбавки
        self.assertEqual(cost, 700)

    def test_weight_20kg_has_50_percent_surcharge(self):
        cost, _ = calculate_delivery_cost(20.0, 100, "обычный") # от 20 кг коэфф. 1,5: (200+500)*1,5 = 1050
        self.assertEqual(cost, 1050)

    """Надбавки за тип посылки"""
class TestPackageTypeSurcharge(unittest.TestCase):
    def test_fragile_adds_300(self):
        cost, _ = calculate_delivery_cost(1, 100, "хрупкий") # хрупкая +300 руб.
        self.assertEqual(cost, 1000)

    def test_dangerous_adds_1000(self):
        cost, _ = calculate_delivery_cost(1, 100, "опасный") # опасный +1000 руб.
        self.assertEqual(cost, 1700)

    """Срочная доставка"""
class TestExpressDelivery(unittest.TestCase):
    def test_express_increases_cost(self):
        normal, _ = calculate_delivery_cost(1, 100, "обычный", is_express=False) # экспресс должен быть дороже обычной доставки
        express, _ = calculate_delivery_cost(1, 100, "обычный", is_express=True)
        self.assertGreater(express, normal)          

    """Расчёт даты доставки"""
class TestDeliveryDate(unittest.TestCase):
    def test_short_distance_one_day(self):
        _, date = calculate_delivery_cost(1, 100, "обычный")# 100км = 1день = 2026.09.04
        self.assertEqual(date, "2026-09-04")

    def test_501km_two_days(self):
        _, date = calculate_delivery_cost(1, 501, "обычный") # 501км = 2 дня(округляется к большему)
        self.assertEqual(date, "2026-09-05")          


if __name__ == "__main__":
    unittest.main()