"""
RAYZEN AI
Browser Agent Integration Tests

Version : 0.1.0
"""

import unittest
from unittest.mock import MagicMock
from src.core.skill_registry import SkillRegistry
from src.browser.playwright_engine import PlaywrightEngine
from src.browser.page_controller import PageController
from src.browser.element_engine import ElementEngine
from src.browser.workflow_runner import WorkflowRunner
from src.agents.browser.browser_agent import BrowserAgent


class TestBrowserAgentIntegration(unittest.TestCase):
    """Integration test suite for BrowserAgent wired to standard dependencies registry."""

    def setUp(self):
        self.registry = SkillRegistry()

        # Mock core browser sub-engines
        self.mock_playwright = MagicMock(spec=PlaywrightEngine)
        self.mock_page_control = MagicMock(spec=PageController)
        self.mock_element_engine = MagicMock(spec=ElementEngine)
        self.mock_runner = MagicMock(spec=WorkflowRunner)

        # Register sub-engines
        self.registry.register("playwright_engine", self.mock_playwright)
        self.registry.register("page_controller", self.mock_page_control)
        self.registry.register("element_engine", self.mock_element_engine)
        self.registry.register("workflow_runner", self.mock_runner)

        self.agent = BrowserAgent(self.registry)

    def test_routing_integration_workflow(self):
        # Configure expectations
        self.mock_playwright.is_browser_running.return_value = False
        self.mock_playwright.launch_browser.return_value = True
        self.mock_page_control.get_current_url.return_value = "https://www.google.com"
        self.mock_page_control.get_page_title.return_value = "Google"

        self.mock_element_engine.exists.return_value = True
        self.mock_runner.validate.return_value = True
        self.mock_runner.execute_step.return_value = True

        # Run query matching google search planning flow
        result = self.agent.execute("search RAYZEN AI project")
        self.assertTrue(result)

        # Verify steps monitor executed sub-runner functions
        self.mock_playwright.launch_browser.assert_called_once_with(headless=False)
        self.assertTrue(self.mock_runner.execute_step.call_count >= 1)

        history = self.agent.get_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].status, "success")
        self.assertIn("type", history[0].steps)


if __name__ == "__main__":
    unittest.main()
