import unittest
from unittest.mock import MagicMock, patch
from src.core.command_engine import CommandEngine
from src.desktop.launcher import DesktopLauncher
from src.browser.controller import BrowserController
from src.core.logger import RayzenLogger


class TestCommandEngine(unittest.TestCase):
    """Test cases for CommandEngine."""

    def setUp(self):
        self.mock_desktop = MagicMock(spec=DesktopLauncher)
        self.mock_browser = MagicMock(spec=BrowserController)
        self.mock_logger = MagicMock(spec=RayzenLogger)
        # Mock underlying logger within RayzenLogger
        self.mock_logger.logger = MagicMock()

        self.engine = CommandEngine(
            desktop_launcher=self.mock_desktop,
            browser_controller=self.mock_browser,
            logger=self.mock_logger,
        )

    def test_execute_notepad_success(self):
        self.mock_desktop.open_notepad.return_value = True
        result = self.engine.execute("open notepad")
        self.assertTrue(result)
        self.mock_desktop.open_notepad.assert_called_once()

    def test_execute_calculator_success(self):
        self.mock_desktop.open_calculator.return_value = True
        result = self.engine.execute("  OPEN CALCULATOR  ")  # test trimming and casing
        self.assertTrue(result)
        self.mock_desktop.open_calculator.assert_called_once()

    def test_execute_explorer_success(self):
        self.mock_desktop.open_explorer.return_value = True
        result = self.engine.execute("open explorer")
        self.assertTrue(result)
        self.mock_desktop.open_explorer.assert_called_once()

    def test_execute_paint_success(self):
        self.mock_desktop.open_paint.return_value = True
        result = self.engine.execute("open paint")
        self.assertTrue(result)
        self.mock_desktop.open_paint.assert_called_once()

    def test_execute_google_success(self):
        self.mock_browser.open_google.return_value = True
        result = self.engine.execute("open google")
        self.assertTrue(result)
        self.mock_browser.open_google.assert_called_once()

    def test_execute_github_success(self):
        self.mock_browser.open_github.return_value = True
        result = self.engine.execute("open github")
        self.assertTrue(result)
        self.mock_browser.open_github.assert_called_once()

    def test_execute_chatgpt_success(self):
        self.mock_browser.open_chatgpt.return_value = True
        result = self.engine.execute("open chatgpt")
        self.assertTrue(result)
        self.mock_browser.open_chatgpt.assert_called_once()

    def test_execute_handler_raises_exception(self):
        self.mock_desktop.open_notepad.side_effect = Exception("Process launch error")
        result = self.engine.execute("open notepad")
        self.assertFalse(result)
        self.mock_logger.error.assert_called_once()

    def test_execute_unknown_command(self):
        result = self.engine.execute("open unknown_app")
        self.assertFalse(result)
        self.mock_logger.logger.warning.assert_called_once_with(
            "Unknown command: 'open unknown_app'"
        )

    def test_execute_invalid_type(self):
        result = self.engine.execute(None)  # type: ignore
        self.assertFalse(result)
        self.mock_logger.error.assert_called_once_with(
            "Command execution failed: Command must be a string."
        )


if __name__ == "__main__":
    unittest.main()
