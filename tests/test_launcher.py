import unittest
from unittest.mock import patch, MagicMock
from src.desktop.launcher import DesktopLauncher


class TestDesktopLauncher(unittest.TestCase):
    """Test cases for DesktopLauncher."""

    def setUp(self):
        self.launcher = DesktopLauncher()

    @patch("subprocess.Popen")
    def test_open_notepad_success(self, mock_popen):
        mock_process = MagicMock()
        mock_popen.return_value = mock_process

        result = self.launcher.open_notepad()
        self.assertTrue(result)
        mock_popen.assert_called_once_with("notepad.exe")

    @patch("subprocess.Popen")
    def test_open_notepad_failure(self, mock_popen):
        mock_popen.side_effect = OSError("Executable not found")

        result = self.launcher.open_notepad()
        self.assertFalse(result)
        mock_popen.assert_called_once_with("notepad.exe")

    @patch("subprocess.Popen")
    def test_open_calculator_success(self, mock_popen):
        mock_process = MagicMock()
        mock_popen.return_value = mock_process

        result = self.launcher.open_calculator()
        self.assertTrue(result)
        mock_popen.assert_called_once_with("calc.exe")

    @patch("subprocess.Popen")
    def test_open_calculator_failure(self, mock_popen):
        mock_popen.side_effect = OSError("Executable not found")

        result = self.launcher.open_calculator()
        self.assertFalse(result)
        mock_popen.assert_called_once_with("calc.exe")

    @patch("subprocess.Popen")
    def test_open_explorer_success(self, mock_popen):
        mock_process = MagicMock()
        mock_popen.return_value = mock_process

        result = self.launcher.open_explorer()
        self.assertTrue(result)
        mock_popen.assert_called_once_with("explorer.exe")

    @patch("subprocess.Popen")
    def test_open_explorer_failure(self, mock_popen):
        mock_popen.side_effect = OSError("Executable not found")

        result = self.launcher.open_explorer()
        self.assertFalse(result)
        mock_popen.assert_called_once_with("explorer.exe")

    @patch("subprocess.Popen")
    def test_open_paint_success(self, mock_popen):
        mock_process = MagicMock()
        mock_popen.return_value = mock_process

        result = self.launcher.open_paint()
        self.assertTrue(result)
        mock_popen.assert_called_once_with("mspaint.exe")

    @patch("subprocess.Popen")
    def test_open_paint_failure(self, mock_popen):
        mock_popen.side_effect = OSError("Executable not found")

        result = self.launcher.open_paint()
        self.assertFalse(result)
        mock_popen.assert_called_once_with("mspaint.exe")


if __name__ == "__main__":
    unittest.main()
