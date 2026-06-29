import os
import unittest
from unittest.mock import patch, MagicMock
from src.browser.playwright_engine import PlaywrightEngine
from src.browser.session_manager import SessionManager


class TestSessionManager(unittest.TestCase):
    """Test cases for SessionManager."""

    def setUp(self):
        self.mock_engine = MagicMock(spec=PlaywrightEngine)
        self.mock_logger = MagicMock()
        self.mock_engine.logger = self.mock_logger
        self.manager = SessionManager(self.mock_engine)

    def test_create_context_browser_not_running(self):
        self.mock_engine.is_browser_running.return_value = False
        result = self.manager.create_context("test_profile")
        self.assertFalse(result)
        self.mock_logger.error.assert_called_once()

    def test_create_context_success(self):
        self.mock_engine.is_browser_running.return_value = True
        mock_browser = MagicMock()
        mock_context = MagicMock()
        self.mock_engine._browser = mock_browser
        mock_browser.contexts = [mock_context]

        result = self.manager.create_context("test_profile")
        self.assertTrue(result)
        self.assertEqual(self.manager.current_profile(), "test_profile")

        expected_path = os.path.join("data/browser_profiles", "test_profile.json")
        mock_context.storage_state.assert_called_once_with(path=expected_path)

    @patch("os.path.exists")
    def test_load_context_does_not_exist(self, mock_exists):
        mock_exists.return_value = False
        result = self.manager.load_context("nonexistent")
        self.assertFalse(result)
        self.mock_logger.error.assert_called_once()

    @patch("os.path.exists")
    def test_load_context_success(self, mock_exists):
        mock_exists.return_value = True
        self.mock_engine.is_browser_running.return_value = True

        mock_browser = MagicMock()
        mock_old_context = MagicMock()
        mock_new_context = MagicMock()
        mock_new_page = MagicMock()

        self.mock_engine._browser = mock_browser
        self.mock_engine._page = MagicMock()
        mock_browser.contexts = [mock_old_context]
        mock_browser.new_context.return_value = mock_new_context
        mock_new_context.new_page.return_value = mock_new_page

        result = self.manager.load_context("test_profile")

        self.assertTrue(result)
        self.assertEqual(self.manager.current_profile(), "test_profile")
        self.assertEqual(self.mock_engine._page, mock_new_page)

        expected_path = os.path.join("data/browser_profiles", "test_profile.json")
        mock_browser.new_context.assert_called_once_with(storage_state=expected_path)
        mock_old_context.close.assert_called_once()

    def test_clear_context_success(self):
        self.mock_engine.is_browser_running.return_value = True
        mock_browser = MagicMock()
        mock_old_context = MagicMock()
        mock_new_context = MagicMock()
        mock_new_page = MagicMock()

        self.mock_engine._browser = mock_browser
        self.mock_engine._page = MagicMock()
        mock_browser.contexts = [mock_old_context]
        mock_browser.new_context.return_value = mock_new_context
        mock_new_context.new_page.return_value = mock_new_page

        result = self.manager.clear_context()

        self.assertTrue(result)
        self.assertEqual(self.manager.current_profile(), "")
        self.assertEqual(self.mock_engine._page, mock_new_page)
        mock_old_context.close.assert_called_once()
        mock_browser.new_context.assert_called_once()

    @patch("os.listdir")
    def test_list_profiles(self, mock_listdir):
        mock_listdir.return_value = ["profile1.json", "profile2.json", "other_file.txt"]

        profiles = self.manager.list_profiles()
        self.assertEqual(profiles, ["profile1", "profile2"])

    def test_is_logged_in_true(self):
        self.mock_engine.is_browser_running.return_value = True
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_context.cookies.return_value = [{"name": "session_id", "value": "123"}]
        self.mock_engine._browser = mock_browser
        mock_browser.contexts = [mock_context]

        self.assertTrue(self.manager.is_logged_in())

    def test_is_logged_in_false(self):
        self.mock_engine.is_browser_running.return_value = True
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_context.cookies.return_value = []
        self.mock_engine._browser = mock_browser
        mock_browser.contexts = [mock_context]

        self.assertFalse(self.manager.is_logged_in())


if __name__ == "__main__":
    unittest.main()
