import unittest
from unittest.mock import MagicMock
from src.browser.playwright_engine import PlaywrightEngine
from src.browser.page_controller import PageController


class TestPageController(unittest.TestCase):
    """Test cases for PageController."""

    def setUp(self):
        self.mock_engine = MagicMock(spec=PlaywrightEngine)
        self.mock_logger = MagicMock()
        self.mock_engine.logger = self.mock_logger
        self.controller = PageController(self.mock_engine)

    def test_new_tab_browser_not_running(self):
        self.mock_engine.is_browser_running.return_value = False
        result = self.controller.new_tab()
        self.assertFalse(result)
        self.mock_logger.error.assert_called_once()

    def test_new_tab_success(self):
        self.mock_engine.is_browser_running.return_value = True

        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()

        self.mock_engine._browser = mock_browser
        mock_browser.contexts = [mock_context]
        mock_context.new_page.return_value = mock_page

        result = self.controller.new_tab()
        self.assertTrue(result)
        self.assertEqual(self.mock_engine._page, mock_page)
        mock_context.new_page.assert_called_once()

    def test_close_current_tab_success(self):
        self.mock_engine.is_browser_running.return_value = True

        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page1 = MagicMock()
        mock_page2 = MagicMock()

        self.mock_engine._browser = mock_browser
        self.mock_engine._page = mock_page2

        mock_browser.contexts = [mock_context]
        mock_context.pages = [mock_page1, mock_page2]

        mock_page1.is_closed.return_value = False
        mock_page2.is_closed.return_value = True

        result = self.controller.close_current_tab()
        self.assertTrue(result)
        mock_page2.close.assert_called_once()
        self.assertEqual(self.mock_engine._page, mock_page1)

    def test_switch_to_tab_out_of_range(self):
        self.mock_engine.is_browser_running.return_value = True
        mock_browser = MagicMock()
        mock_context = MagicMock()

        self.mock_engine._browser = mock_browser
        mock_browser.contexts = [mock_context]
        mock_context.pages = [MagicMock()]

        result = self.controller.switch_to_tab(5)
        self.assertFalse(result)
        self.mock_logger.error.assert_called_once()

    def test_switch_to_tab_success(self):
        self.mock_engine.is_browser_running.return_value = True
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page1 = MagicMock()
        mock_page2 = MagicMock()

        self.mock_engine._browser = mock_browser
        mock_browser.contexts = [mock_context]
        mock_context.pages = [mock_page1, mock_page2]

        result = self.controller.switch_to_tab(1)
        self.assertTrue(result)
        self.assertEqual(self.mock_engine._page, mock_page2)

    def test_refresh_page(self):
        self.mock_engine.is_browser_running.return_value = True
        mock_page = MagicMock()
        self.mock_engine._page = mock_page

        result = self.controller.refresh_page()
        self.assertTrue(result)
        mock_page.reload.assert_called_once()

    def test_go_back(self):
        self.mock_engine.is_browser_running.return_value = True
        mock_page = MagicMock()
        self.mock_engine._page = mock_page

        result = self.controller.go_back()
        self.assertTrue(result)
        mock_page.go_back.assert_called_once()

    def test_go_forward(self):
        self.mock_engine.is_browser_running.return_value = True
        mock_page = MagicMock()
        self.mock_engine._page = mock_page

        result = self.controller.go_forward()
        self.assertTrue(result)
        mock_page.go_forward.assert_called_once()

    def test_get_current_url(self):
        self.mock_engine.is_browser_running.return_value = True
        mock_page = MagicMock()
        mock_page.url = "https://example.com"
        self.mock_engine._page = mock_page

        url = self.controller.get_current_url()
        self.assertEqual(url, "https://example.com")

    def test_get_page_title(self):
        self.mock_engine.is_browser_running.return_value = True
        mock_page = MagicMock()
        mock_page.title.return_value = "Example Title"
        self.mock_engine._page = mock_page

        title = self.controller.get_page_title()
        self.assertEqual(title, "Example Title")

    def test_list_open_tabs(self):
        self.mock_engine.is_browser_running.return_value = True
        mock_browser = MagicMock()
        mock_context = MagicMock()

        self.mock_engine._browser = mock_browser
        mock_browser.contexts = [mock_context]

        mock_page1 = MagicMock()
        mock_page1.url = "https://page1.com"
        mock_page2 = MagicMock()
        mock_page2.url = "https://page2.com"
        mock_context.pages = [mock_page1, mock_page2]

        tabs = self.controller.list_open_tabs()
        self.assertEqual(tabs, ["https://page1.com", "https://page2.com"])


if __name__ == "__main__":
    unittest.main()
