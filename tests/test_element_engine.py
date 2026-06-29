import unittest
from unittest.mock import MagicMock
from src.browser.playwright_engine import PlaywrightEngine
from src.browser.element_engine import ElementEngine


class TestElementEngine(unittest.TestCase):
    """Test cases for ElementEngine."""

    def setUp(self):
        self.mock_engine = MagicMock(spec=PlaywrightEngine)
        self.mock_logger = MagicMock()
        self.mock_engine.logger = self.mock_logger
        self.engine = ElementEngine(self.mock_engine)

    def test_click_success(self):
        self.mock_engine.is_browser_running.return_value = True
        mock_page = MagicMock()
        self.mock_engine._page = mock_page

        result = self.engine.click(".btn")
        self.assertTrue(result)
        mock_page.click.assert_called_once_with(".btn")

    def test_click_failed_browser_not_running(self):
        self.mock_engine.is_browser_running.return_value = False

        result = self.engine.click(".btn")
        self.assertFalse(result)
        self.mock_logger.error.assert_called_once()

    def test_type_text_success(self):
        self.mock_engine.is_browser_running.return_value = True
        mock_page = MagicMock()
        self.mock_engine._page = mock_page

        result = self.engine.type_text("#input", "hello")
        self.assertTrue(result)
        mock_page.fill.assert_called_once_with("#input", "hello")

    def test_clear_success(self):
        self.mock_engine.is_browser_running.return_value = True
        mock_page = MagicMock()
        self.mock_engine._page = mock_page

        result = self.engine.clear("#input")
        self.assertTrue(result)
        mock_page.fill.assert_called_once_with("#input", "")

    def test_press_key_success(self):
        self.mock_engine.is_browser_running.return_value = True
        mock_page = MagicMock()
        self.mock_engine._page = mock_page

        result = self.engine.press_key("Enter")
        self.assertTrue(result)
        mock_page.keyboard.press.assert_called_once_with("Enter")

    def test_hover_success(self):
        self.mock_engine.is_browser_running.return_value = True
        mock_page = MagicMock()
        self.mock_engine._page = mock_page

        result = self.engine.hover(".menu")
        self.assertTrue(result)
        mock_page.hover.assert_called_once_with(".menu")

    def test_scroll_to_success(self):
        self.mock_engine.is_browser_running.return_value = True
        mock_page = MagicMock()
        mock_locator = MagicMock()
        self.mock_engine._page = mock_page
        mock_page.locator.return_value = mock_locator

        result = self.engine.scroll_to(".footer")
        self.assertTrue(result)
        mock_page.locator.assert_called_once_with(".footer")
        mock_locator.scroll_into_view_if_needed.assert_called_once()

    def test_wait_for_success(self):
        self.mock_engine.is_browser_running.return_value = True
        mock_page = MagicMock()
        self.mock_engine._page = mock_page

        result = self.engine.wait_for(".popup", 5000)
        self.assertTrue(result)
        mock_page.wait_for_selector.assert_called_once_with(".popup", timeout=5000)

    def test_get_text_success(self):
        self.mock_engine.is_browser_running.return_value = True
        mock_page = MagicMock()
        mock_locator = MagicMock()
        mock_locator.inner_text.return_value = "hello world"
        self.mock_engine._page = mock_page
        mock_page.locator.return_value = mock_locator

        text = self.engine.get_text(".content")
        self.assertEqual(text, "hello world")
        mock_locator.inner_text.assert_called_once()

    def test_get_html_success(self):
        self.mock_engine.is_browser_running.return_value = True
        mock_page = MagicMock()
        mock_locator = MagicMock()
        mock_locator.inner_html.return_value = "<span>hello</span>"
        self.mock_engine._page = mock_page
        mock_page.locator.return_value = mock_locator

        html = self.engine.get_html(".content")
        self.assertEqual(html, "<span>hello</span>")
        mock_locator.inner_html.assert_called_once()

    def test_exists_true(self):
        self.mock_engine.is_browser_running.return_value = True
        mock_page = MagicMock()
        mock_locator = MagicMock()
        mock_locator.count.return_value = 1
        self.mock_engine._page = mock_page
        mock_page.locator.return_value = mock_locator

        result = self.engine.exists(".content")
        self.assertTrue(result)
        mock_locator.count.assert_called_once()

    def test_exists_false(self):
        self.mock_engine.is_browser_running.return_value = True
        mock_page = MagicMock()
        mock_locator = MagicMock()
        mock_locator.count.return_value = 0
        self.mock_engine._page = mock_page
        mock_page.locator.return_value = mock_locator

        result = self.engine.exists(".content")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
