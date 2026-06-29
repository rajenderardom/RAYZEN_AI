import unittest
from unittest.mock import MagicMock, patch
from src.browser.playwright_engine import PlaywrightEngine
from src.browser.element_engine import ElementEngine
from src.browser.page_controller import PageController
from src.browser.workflow_runner import WorkflowRunner


class TestWorkflowRunner(unittest.TestCase):
    """Test cases for WorkflowRunner."""

    def setUp(self):
        self.mock_playwright = MagicMock(spec=PlaywrightEngine)
        self.mock_element = MagicMock(spec=ElementEngine)
        self.mock_page_control = MagicMock(spec=PageController)

        self.mock_logger = MagicMock()
        self.mock_playwright.logger = self.mock_logger

        self.runner = WorkflowRunner(
            playwright_engine=self.mock_playwright,
            element_engine=self.mock_element,
            page_controller=self.mock_page_control,
        )

    def test_validate_step_success(self):
        step = {"action": "open_url", "url": "https://example.com"}
        self.assertTrue(self.runner.validate(step))

    def test_validate_step_missing_param(self):
        step = {"action": "type", "selector": "#input"}  # missing 'text'
        self.assertFalse(self.runner.validate(step))

    def test_validate_step_unknown_action(self):
        step = {"action": "invalid_action"}
        self.assertFalse(self.runner.validate(step))

    def test_execute_step_open_url(self):
        self.mock_playwright.open_url.return_value = True
        step = {"action": "open_url", "url": "https://google.com"}

        result = self.runner.execute_step(step)
        self.assertTrue(result)
        self.mock_playwright.open_url.assert_called_once_with("https://google.com")

    def test_execute_step_click(self):
        self.mock_element.click.return_value = True
        step = {"action": "click", "selector": ".submit-btn"}

        result = self.runner.execute_step(step)
        self.assertTrue(result)
        self.mock_element.click.assert_called_once_with(".submit-btn")

    @patch("time.sleep")
    def test_execute_step_wait(self, mock_sleep):
        step = {"action": "wait", "duration": 2000}
        result = self.runner.execute_step(step)

        self.assertTrue(result)
        mock_sleep.assert_called_once_with(2.0)

    def test_execute_step_screenshot(self):
        self.mock_playwright.is_browser_running.return_value = True
        mock_page = MagicMock()
        self.mock_playwright._page = mock_page

        step = {"action": "screenshot", "path": "test.png"}
        result = self.runner.execute_step(step)

        self.assertTrue(result)
        mock_page.screenshot.assert_called_once_with(path="test.png")

    def test_execute_step_verify_text_success(self):
        self.mock_element.get_text.return_value = "Hello World"
        step = {"action": "verify", "selector": "#title", "text": "Hello"}

        result = self.runner.execute_step(step)
        self.assertTrue(result)
        self.mock_element.get_text.assert_called_once_with("#title")

    def test_execute_step_verify_text_failure(self):
        self.mock_element.get_text.return_value = "Goodbye World"
        step = {"action": "verify", "selector": "#title", "text": "Hello"}

        result = self.runner.execute_step(step)
        self.assertFalse(result)

    def test_execute_step_verify_exists_success(self):
        self.mock_element.exists.return_value = True
        step = {"action": "verify", "selector": "#title"}

        result = self.runner.execute_step(step)
        self.assertTrue(result)
        self.mock_element.exists.assert_called_once_with("#title")

    def test_execute_step_verify_exists_failure(self):
        self.mock_element.exists.return_value = False
        step = {"action": "verify", "selector": "#title"}

        result = self.runner.execute_step(step)
        self.assertFalse(result)

    def test_run_workflow_halt_on_failure(self):
        self.mock_playwright.open_url.return_value = True
        self.mock_element.click.return_value = False  # Click fails

        workflow = [
            {"action": "open_url", "url": "https://google.com"},
            {"action": "click", "selector": ".bad-btn"},
            {"action": "refresh"},
        ]

        result = self.runner.run(workflow)
        self.assertFalse(result)
        self.mock_playwright.open_url.assert_called_once()
        self.mock_element.click.assert_called_once()
        self.mock_page_control.refresh_page.assert_not_called()  # Halts early


if __name__ == "__main__":
    unittest.main()
