import unittest
from unittest.mock import patch
from src.browser.controller import BrowserController


class TestBrowserController(unittest.TestCase):
    """Test cases for BrowserController."""

    def setUp(self):
        self.controller = BrowserController()

    @patch("webbrowser.open")
    def test_open_default_browser_success(self, mock_open):
        mock_open.return_value = True
        result = self.controller.open_default_browser("https://example.com")
        self.assertTrue(result)
        mock_open.assert_called_once_with("https://example.com")

    @patch("webbrowser.open")
    def test_open_default_browser_failure(self, mock_open):
        mock_open.return_value = False
        result = self.controller.open_default_browser("https://example.com")
        self.assertFalse(result)
        mock_open.assert_called_once_with("https://example.com")

    @patch("webbrowser.open")
    def test_open_default_browser_exception(self, mock_open):
        mock_open.side_effect = Exception("Browser launch error")
        result = self.controller.open_default_browser("https://example.com")
        self.assertFalse(result)
        mock_open.assert_called_once_with("https://example.com")

    @patch("webbrowser.open")
    def test_open_google(self, mock_open):
        mock_open.return_value = True
        result = self.controller.open_google()
        self.assertTrue(result)
        mock_open.assert_called_once_with("https://www.google.com")

    @patch("webbrowser.open")
    def test_open_github(self, mock_open):
        mock_open.return_value = True
        result = self.controller.open_github()
        self.assertTrue(result)
        mock_open.assert_called_once_with("https://github.com")

    @patch("webbrowser.open")
    def test_open_chatgpt(self, mock_open):
        mock_open.return_value = True
        result = self.controller.open_chatgpt()
        self.assertTrue(result)
        mock_open.assert_called_once_with("https://chatgpt.com")


if __name__ == "__main__":
    unittest.main()
