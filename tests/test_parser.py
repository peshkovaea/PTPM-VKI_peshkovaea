import unittest
from pathlib import Path
from src.parser import ForumParser
from src.database import DatabaseRepository

class TestForumParser(unittest.TestCase):
    def setUp(self):
        self.parser = ForumParser()
        # Загружаем HTML из файла 
        fixture_path = Path(__file__).parent / 'fixtures' / 'page.html'
        self.html = fixture_path.read_text(encoding='utf-8')

    def test_parse_html_structure(self):
        # Проверка корректности извлечения данных
        data = self.parser.parse_html(self.html)
        self.assertGreater(len(data), 0)
        
        first_item = data[0]
        self.assertIsInstance(first_item['id'], int)
        self.assertTrue(len(first_item['name']) > 0)
        self.assertTrue(len(first_item['message']) > 0)

    def test_save_to_db(self):
        # Проверка сохранения в БД
        repo = DatabaseRepository(":memory:")
        data = self.parser.parse_html(self.html)
        saved_count = self.parser.save_to_db(data, repo)
        
        self.assertGreater(saved_count, 0)
        # Проверяем, что первая запись действительно попала в БД
        first_id = data[0]['id']
        self.assertIsNotNone(repo.get_by_id(first_id))

if __name__ == "__main__":
    unittest.main()