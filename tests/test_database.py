import unittest
from src.database import DatabaseRepository

class TestDatabaseRepository(unittest.TestCase):
    def setUp(self):
        self.repo = DatabaseRepository(":memory:") # новая БД перед каждым тестом

    def tearDown(self): # после тестов 
        self.repo.close()

    # тесты для add (успех + дублирование ID)
    def test_add_success(self):
        self.assertTrue(self.repo.add(1, "alice", "Привет!"))

    def test_add_duplicate_id_raises(self):
        self.repo.add(1, "alice", "Привет!")
        with self.assertRaises(Exception):
            self.repo.add(1, "bob", "Другое")

    # тесты для get_by_id (найдено + не найдено)
    def test_get_by_id_found(self):
        self.repo.add(5, "carol", "Hi")
        self.assertEqual(self.repo.get_by_id(5)["name"], "carol")

    def test_get_by_id_not_found(self):
        self.assertIsNone(self.repo.get_by_id(999))

    # тесты для get_by_name (несколько записей + пустой результат)
    def test_get_by_name_multiple(self):
        self.repo.add(1, "dave", "one")
        self.repo.add(2, "dave", "two")
        self.assertEqual(len(self.repo.get_by_name("dave")), 2)

    def test_get_by_name_empty(self):
        self.assertEqual(self.repo.get_by_name("nobody"), [])

    # тесты для update (успех + несуществующий ID)
    def test_update_success(self):
        self.repo.add(1, "alice", "old")
        self.assertTrue(self.repo.update(1, "new"))
        self.assertEqual(self.repo.get_by_id(1)["message"], "new")

    def test_update_missing_id_raises(self):
        with self.assertRaises(LookupError):
            self.repo.update(42, "new")

    # тесты для delete (успех + несуществующий ID)
    def test_delete_success(self):
        self.repo.add(1, "alice", "hi")
        self.assertTrue(self.repo.delete(1))
        self.assertIsNone(self.repo.get_by_id(1))

    def test_delete_missing_returns_false(self):
        self.assertFalse(self.repo.delete(999))

if __name__ == "__main__":
    unittest.main()