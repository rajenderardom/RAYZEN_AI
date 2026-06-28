import unittest
from src.core.interpreter import NaturalLanguageInterpreter


class TestNaturalLanguageInterpreter(unittest.TestCase):
    """Test cases for NaturalLanguageInterpreter."""

    def setUp(self):
        self.interpreter = NaturalLanguageInterpreter()

    def test_interpret_google_kholo(self):
        self.assertEqual(self.interpreter.interpret("google kholo"), "open google")
        self.assertEqual(self.interpreter.interpret("  GOOGLE KHOLO  "), "open google")

    def test_interpret_calculator_kholo(self):
        self.assertEqual(self.interpreter.interpret("calculator kholo"), "open calculator")
        self.assertEqual(self.interpreter.interpret("Calculator Kholo"), "open calculator")

    def test_interpret_chatgpt_kholo(self):
        self.assertEqual(self.interpreter.interpret("chatgpt kholo"), "open chatgpt")

    def test_interpret_paint_kholo(self):
        self.assertEqual(self.interpreter.interpret("paint kholo"), "open paint")

    def test_interpret_open_my_browser(self):
        self.assertEqual(self.interpreter.interpret("open my browser"), "open google")
        self.assertEqual(self.interpreter.interpret("Open My Browser"), "open google")

    def test_interpret_unknown_command(self):
        # Unknown inputs should return the original text unchanged
        unknown = "launch command prompt"
        self.assertEqual(self.interpreter.interpret(unknown), unknown)

        unknown_case_spacing = "  Launch Command Prompt  "
        self.assertEqual(self.interpreter.interpret(unknown_case_spacing), unknown_case_spacing)

    def test_interpret_invalid_type(self):
        self.assertIsNone(self.interpreter.interpret(None))  # type: ignore
        self.assertEqual(self.interpreter.interpret(12345), 12345)  # type: ignore


if __name__ == "__main__":
    unittest.main()
