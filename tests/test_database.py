import unittest
from src.database import TriangleDB


class TestTriangleDB(unittest.TestCase):
    def setUp(self):
        self.db = TriangleDB(":memory:")

    def test_add_and_get(self):
        self.db.add(3, 4, 5, "разносторонний", "")
        row = self.db.get(3, 4, 5)
        self.assertIsNotNone(row)
        self.assertEqual(row[0], "разносторонний")
        self.assertEqual(row[1], "")

    def test_get_missing_returns_none(self):
        self.assertIsNone(self.db.get(1, 1, 1))

    def test_delete(self):
        self.db.add(3, 4, 5, "разносторонний", "")
        self.db.delete(3, 4, 5)
        self.assertIsNone(self.db.get(3, 4, 5))

    def test_add_overwrites_existing(self):
        self.db.add(3, 4, 5, "разносторонний", "")
        self.db.add(3, 4, 5, "равнобедренный", "")
        row = self.db.get(3, 4, 5)
        self.assertEqual(row[0], "равнобедренный")


if __name__ == "__main__":
    unittest.main()