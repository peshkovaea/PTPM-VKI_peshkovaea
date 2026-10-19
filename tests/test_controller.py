import unittest
from unittest.mock import Mock
from src.controller import Controller
from src.database import TriangleDB
from src.calculator import TriangleCalculator
from src.notifier import Notifier


class TestControllerIntegration(unittest.TestCase):
    def setUp(self):
        self.io = Mock()
        self.io.get_input.side_effect = ["3", "4", "5"]
        self.db = TriangleDB(":memory:")
        self.calc = Mock(wraps=TriangleCalculator())
        self.notifier = Mock(spec=Notifier)
        self.controller = Controller(self.io, self.db, self.calc, self.notifier)

    def test_controller_sends_result_to_notifier(self):
        result = self.controller.run()
        self.notifier.send.assert_called_once()
        sent_message = self.notifier.send.call_args[0][0]
        self.assertIn("разносторонний", sent_message)
        self.assertIn("разносторонний", result)

    def test_controller_saves_to_db(self):
        self.controller.run()
        row = self.db.get(3, 4, 5)
        self.assertIsNotNone(row)
        self.assertEqual(row[0], "разносторонний")
        self.assertEqual(row[1], "")

    def test_controller_uses_cache_on_second_run(self):
        self.controller.run()
        self.assertEqual(self.calc.determine_type.call_count, 1)

        self.io.get_input.side_effect = ["3", "4", "5"]
        self.controller.run()
        self.assertEqual(self.calc.determine_type.call_count, 1)
        self.assertEqual(self.notifier.send.call_count, 2)


if __name__ == "__main__":
    unittest.main()