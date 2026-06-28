import unittest
from unittest.mock import patch, MagicMock
from src.core.app import RayzenApp


class TestIntegration(unittest.TestCase):
    """Integration test cases connecting RayzenApp, Interpreter, and CommandEngine."""

    @patch("builtins.input")
    @patch("builtins.print")
    @patch("subprocess.Popen")
    @patch("webbrowser.open")
    def test_pipeline_natural_language_to_subsystems(
        self, mock_web_open, mock_popen, mock_print, mock_input
    ):
        # Sequence of inputs simulating a user typing various natural language queries
        mock_input.side_effect = [
            "google kholo",
            "calculator kholo",
            "open my browser",
            "notepad kholo",
            "unknown text input",
            "exit",
        ]

        mock_web_open.return_value = True
        mock_popen.return_value = MagicMock()

        app = RayzenApp()
        app.start()

        # Check browser opens for google kholo and open my browser
        self.assertEqual(mock_web_open.call_count, 2)
        mock_web_open.assert_any_call("https://www.google.com")

        # Check notepad and calculator launcher calls
        self.assertEqual(mock_popen.call_count, 2)
        mock_popen.assert_any_call("calc.exe")
        mock_popen.assert_any_call("notepad.exe")

        # Verify that "Unknown command." was printed for the unknown input
        unknown_printed = any(
            "Unknown command." in call[0][0]
            for call in mock_print.call_args_list
            if len(call[0]) > 0
        )
        self.assertTrue(unknown_printed)


if __name__ == "__main__":
    unittest.main()
