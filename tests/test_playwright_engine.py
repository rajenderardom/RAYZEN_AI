import unittest
from unittest.mock import patch, MagicMock
from src.browser.playwright_engine import PlaywrightEngine


class TestPlaywrightEngine(unittest.TestCase):
    """Test cases for PlaywrightEngine."""

    def setUp(self):
        self.engine = PlaywrightEngine()

    @patch("src.browser.playwright_engine.sync_playwright")
    def test_launch_browser_success(self, mock_sync_playwright):
        # Setup mock playwright structure
        mock_pw_inst = MagicMock()
        mock_sync_playwright.return_value.start.return_value = mock_pw_inst

        mock_chromium = MagicMock()
        mock_pw_inst.chromium = mock_chromium

        mock_browser = MagicMock()
        mock_chromium.launch.return_value = mock_browser
        mock_browser.is_connected.return_value = True

        mock_context = MagicMock()
        mock_browser.new_context.return_value = mock_context

        mock_page = MagicMock()
        mock_context.new_page.return_value = mock_page

        result = self.engine.launch_browser(headless=True)

        self.assertTrue(result)
        self.assertTrue(self.engine.is_browser_running())
        mock_chromium.launch.assert_called_once_with(headless=True)

    @patch("src.browser.playwright_engine.sync_playwright")
    def test_launch_browser_failure(self, mock_sync_playwright):
        mock_sync_playwright.side_effect = Exception("Initialization error")

        result = self.engine.launch_browser()
        self.assertFalse(result)
        self.assertFalse(self.engine.is_browser_running())

    @patch("src.browser.playwright_engine.sync_playwright")
    def test_open_url_success(self, mock_sync_playwright):
        mock_pw_inst = MagicMock()
        mock_sync_playwright.return_value.start.return_value = mock_pw_inst
        mock_browser = MagicMock()
        mock_pw_inst.chromium.launch.return_value = mock_browser
        mock_browser.is_connected.return_value = True
        mock_page = MagicMock()
        mock_browser.new_context.return_value.new_page.return_value = mock_page

        self.engine.launch_browser()

        result = self.engine.open_url("https://example.com")
        self.assertTrue(result)
        mock_page.goto.assert_called_once_with("https://example.com")

    @patch("src.browser.playwright_engine.sync_playwright")
    def test_open_url_auto_launch(self, mock_sync_playwright):
        mock_pw_inst = MagicMock()
        mock_sync_playwright.return_value.start.return_value = mock_pw_inst
        mock_browser = MagicMock()
        mock_pw_inst.chromium.launch.return_value = mock_browser
        mock_browser.is_connected.return_value = True
        mock_page = MagicMock()
        mock_browser.new_context.return_value.new_page.return_value = mock_page

        # Directly call open_url when not running
        result = self.engine.open_url("https://example.com")
        self.assertTrue(result)
        mock_page.goto.assert_called_once_with("https://example.com")

    @patch("src.browser.playwright_engine.sync_playwright")
    def test_open_url_exception(self, mock_sync_playwright):
        mock_pw_inst = MagicMock()
        mock_sync_playwright.return_value.start.return_value = mock_pw_inst
        mock_browser = MagicMock()
        mock_pw_inst.chromium.launch.return_value = mock_browser
        mock_browser.is_connected.return_value = True
        mock_page = MagicMock()
        mock_browser.new_context.return_value.new_page.return_value = mock_page

        mock_page.goto.side_effect = Exception("Page load error")
        self.engine.launch_browser()

        result = self.engine.open_url("https://example.com")
        self.assertFalse(result)

    @patch("src.browser.playwright_engine.sync_playwright")
    def test_close_browser(self, mock_sync_playwright):
        mock_pw_inst = MagicMock()
        mock_sync_playwright.return_value.start.return_value = mock_pw_inst
        mock_browser = MagicMock()
        mock_pw_inst.chromium.launch.return_value = mock_browser
        mock_browser.is_connected.return_value = True

        self.engine.launch_browser()
        result = self.engine.close_browser()

        self.assertTrue(result)
        mock_browser.close.assert_called_once()
        mock_pw_inst.stop.assert_called_once()
        self.assertFalse(self.engine.is_browser_running())


if __name__ == "__main__":
    unittest.main()
