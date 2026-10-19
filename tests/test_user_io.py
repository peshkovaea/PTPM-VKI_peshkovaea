import unittest
from unittest.mock import patch
from src.user_io import UserIO, ConsoleUserIO


class TestUserIO(unittest.TestCase):
    def test_cannot_instantiate_abstract(self):
        with self.assertRaises(TypeError):
            UserIO()

    @patch("builtins.input", return_value="42")
    def test_console_reads_input(self, mock_input):
        io = ConsoleUserIO()
        result = io.get_input("Введите число: ")
        self.assertEqual(result, "42")
        mock_input.assert_called_once_with("Введите число: ")


if __name__ == "__main__":
    unittest.main()