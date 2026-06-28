import unittest
from unittest.mock import patch, MagicMock
from src.core.app import RayzenApp


class TestRayzenApp(unittest.TestCase):
    """Test cases for RayzenApp interactive console loop."""

    @patch("builtins.input")
    @patch("builtins.print")
    @patch("src.core.app.CommandEngine")
    def test_start_loop_exit_immediately(self, mock_engine_class, mock_print, mock_input):
        mock_input.return_value = "exit"
        app = RayzenApp()
        app.start()

        mock_input.assert_called_once_with("> ")

    @patch("builtins.input")
    @patch("builtins.print")
    def test_start_loop_help(self, mock_print, mock_input):
        # First return "help", then "exit" to terminate the loop
        mock_input.side_effect = ["help", "exit"]
        app = RayzenApp()
        app.start()

        # Verify show_help was called by checking print calls
        help_printed = any(
            "Supported commands:" in call[0][0]
            for call in mock_print.call_args_list
            if len(call[0]) > 0
        )
        self.assertTrue(help_printed)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_start_loop_known_command(self, mock_print, mock_input):
        mock_input.side_effect = ["open notepad", "exit"]
        app = RayzenApp()
        # Mock the execute method of command engine
        app.command_engine.execute = MagicMock(return_value=True)

        app.start()

        app.command_engine.execute.assert_called_once_with("open notepad")

    @patch("builtins.input")
    @patch("builtins.print")
    def test_start_loop_unknown_command(self, mock_print, mock_input):
        mock_input.side_effect = ["invalid_cmd", "exit"]
        app = RayzenApp()
        app.command_engine.execute = MagicMock(return_value=False)

        app.start()

        # It should pass it to command_engine.execute
        app.command_engine.execute.assert_called_once_with("invalid_cmd")
        # It should print "Unknown command."
        unknown_printed = any(
            "Unknown command." in call[0][0]
            for call in mock_print.call_args_list
            if len(call[0]) > 0
        )
        self.assertTrue(unknown_printed)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_start_loop_keyboard_interrupt(self, mock_print, mock_input):
        # KeyboardInterrupt on the first input call should break loop gracefully
        mock_input.side_effect = KeyboardInterrupt
        app = RayzenApp()

        # This shouldn't raise exception
        try:
            app.start()
        except KeyboardInterrupt:
            self.fail("KeyboardInterrupt was not caught by the application loop.")

    @patch("builtins.input")
    @patch("builtins.print")
    def test_start_loop_help_calls_public_api(self, mock_print, mock_input):
        mock_input.side_effect = ["help", "exit"]
        app = RayzenApp()
        app.command_engine.get_available_commands = MagicMock(
            return_value=["mocked notepad", "mocked calc"]
        )

        app.start()

        app.command_engine.get_available_commands.assert_called()
        help_printed = any(
            "- mocked notepad" in call[0][0]
            for call in mock_print.call_args_list
            if len(call[0]) > 0
        )
        self.assertTrue(help_printed)



if __name__ == "__main__":
    unittest.main()
