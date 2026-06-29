"""
RAYZEN AI
Browser Agent Unit Tests

Version : 0.1.0
"""

import os
import unittest
from unittest.mock import MagicMock, patch
from src.core.skill_registry import SkillRegistry
from src.browser.playwright_engine import PlaywrightEngine
from src.browser.page_controller import PageController
from src.browser.element_engine import ElementEngine
from src.browser.workflow_runner import WorkflowRunner
from src.agents.browser.browser_models import BrowserTaskRecord, BrowserAgentState
from src.agents.browser.browser_context import BrowserContext
from src.agents.browser.page_analyzer import PageAnalyzer
from src.agents.browser.action_planner import ActionPlanner
from src.agents.browser.execution_monitor import ExecutionMonitor
from src.agents.browser.recovery_engine import RecoveryEngine
from src.agents.browser.browser_agent import BrowserAgent


class TestBrowserContext(unittest.TestCase):
    """Unit tests for BrowserContext thread-safe states."""

    def test_set_get_clear(self):
        ctx = BrowserContext()
        ctx.set("profile_id", "admin_session")
        self.assertEqual(ctx.get("profile_id"), "admin_session")
        
        ctx.set("active_tab", 2)
        all_vars = ctx.get_all()
        self.assertEqual(all_vars["active_tab"], 2)
        
        ctx.clear()
        self.assertEqual(ctx.get("profile_id"), None)


class TestPageAnalyzer(unittest.TestCase):
    """Unit tests for PageAnalyzer layouts scanning."""

    def test_analyze_page(self):
        mock_page_control = MagicMock(spec=PageController)
        mock_page_control.get_current_url.return_value = "https://example.com/login"
        mock_page_control.get_page_title.return_value = "Portal Login"

        mock_element_engine = MagicMock(spec=ElementEngine)
        # Simulate existence of #username and button
        mock_element_engine.exists.side_effect = lambda s: s in ("#username", "button")

        analyzer = PageAnalyzer()
        res = analyzer.analyze_page(mock_page_control, mock_element_engine)

        self.assertEqual(res["url"], "https://example.com/login")
        self.assertEqual(res["title"], "Portal Login")
        self.assertIn("#username", res["inputs"])
        self.assertIn("button", res["buttons"])


class TestActionPlanner(unittest.TestCase):
    """Unit tests for ActionPlanner workflow planning."""

    def setUp(self):
        self.planner = ActionPlanner()

    def test_plan_explicit_url(self):
        steps = self.planner.plan_actions("Go to https://google.com/search", {})
        self.assertEqual(steps[0]["action"], "open_url")
        self.assertEqual(steps[0]["url"], "https://google.com/search")

    def test_plan_login_intent(self):
        analysis = {
            "inputs": ["#username", "#password"],
            "buttons": ["#submit-btn"],
        }
        steps = self.planner.plan_actions("Please Login to the website", analysis)
        actions = [s["action"] for s in steps]
        self.assertIn("type", actions)
        self.assertIn("click", actions)

    def test_plan_search_intent(self):
        analysis = {
            "inputs": ["input[name='q']"],
            "buttons": [],
        }
        steps = self.planner.plan_actions("search deepmind", analysis)
        self.assertEqual(steps[0]["action"], "type")
        self.assertEqual(steps[0]["text"], "deepmind")


class TestExecutionMonitor(unittest.TestCase):
    """Unit tests for ExecutionMonitor tracking status."""

    def test_execute_monitor_success(self):
        mock_runner = MagicMock(spec=WorkflowRunner)
        mock_runner.validate.return_value = True
        mock_runner.execute_step.return_value = True

        monitor = ExecutionMonitor()
        steps = [{"action": "click", "selector": "button"}]
        res = monitor.execute_and_monitor(mock_runner, steps)
        self.assertTrue(res)

    def test_execute_monitor_validation_failed(self):
        mock_runner = MagicMock(spec=WorkflowRunner)
        mock_runner.validate.return_value = False

        monitor = ExecutionMonitor()
        steps = [{"action": "click", "selector": "button"}]
        res = monitor.execute_and_monitor(mock_runner, steps)
        self.assertFalse(res)


class TestRecoveryEngine(unittest.TestCase):
    """Unit tests for RecoveryEngine reloads and navigation."""

    def test_recovery_strategies(self):
        mock_page_control = MagicMock(spec=PageController)
        mock_page_control.refresh_page.return_value = True
        mock_page_control.go_back.return_value = True

        recovery = RecoveryEngine()
        self.assertTrue(recovery.reload_page(mock_page_control))
        self.assertTrue(recovery.navigate_back(mock_page_control))
        self.assertTrue(recovery.wait_and_retry(100))


class TestBrowserAgent(unittest.TestCase):
    """Unit tests for BrowserAgent core orchestrator flow."""

    def setUp(self):
        self.mock_registry = MagicMock(spec=SkillRegistry)
        self.mock_playwright = MagicMock(spec=PlaywrightEngine)
        self.mock_page_control = MagicMock(spec=PageController)
        self.mock_element_engine = MagicMock(spec=ElementEngine)
        self.mock_runner = MagicMock(spec=WorkflowRunner)

        self.mock_registry.get.side_effect = lambda name: {
            "playwright_engine": self.mock_playwright,
            "page_controller": self.mock_page_control,
            "element_engine": self.mock_element_engine,
            "workflow_runner": self.mock_runner,
        }.get(name)

        self.agent = BrowserAgent(self.mock_registry)

    def test_agent_execute_success(self):
        self.mock_playwright.is_browser_running.return_value = True
        self.mock_page_control.get_current_url.return_value = "https://example.com"
        self.mock_page_control.get_page_title.return_value = "Example Page"
        self.mock_element_engine.exists.return_value = False

        self.mock_runner.validate.return_value = True
        self.mock_runner.execute_step.return_value = True

        result = self.agent.execute("Open URL https://example.com")
        self.assertTrue(result)
        self.assertEqual(len(self.agent.get_history()), 1)
        self.assertEqual(self.agent.get_history()[0].status, "success")

    def test_agent_missing_skills(self):
        # Empty registry
        empty_reg = MagicMock(spec=SkillRegistry)
        empty_reg.get.return_value = None
        agent = BrowserAgent(empty_reg)

        result = agent.execute("Open google")
        self.assertFalse(result)
        self.assertEqual(agent.get_history()[0].status, "failed")


if __name__ == "__main__":
    unittest.main()
