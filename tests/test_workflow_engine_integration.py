import os
import unittest
from unittest.mock import patch, MagicMock
from src.brain.task_planner import TaskPlanner
from src.brain.intent_analyzer import IntentAnalyzer
from src.core.interpreter import NaturalLanguageInterpreter
from src.browser.playwright_engine import PlaywrightEngine
from src.desktop.launcher import DesktopLauncher
from src.excel.manager import ExcelManager
from src.brain.workflow_engine import WorkflowEngine


class TestWorkflowEngineIntegration(unittest.TestCase):
    """Integration test suite for WorkflowEngine executing real workflows."""

    def setUp(self):
        interpreter = NaturalLanguageInterpreter()
        analyzer = IntentAnalyzer(interpreter)
        self.planner = TaskPlanner(analyzer)

        self.mock_browser = MagicMock(spec=PlaywrightEngine)
        self.mock_desktop = MagicMock(spec=DesktopLauncher)
        self.mock_excel = MagicMock(spec=ExcelManager)

        self.mock_logger = MagicMock()
        self.mock_browser.logger = self.mock_logger

        self.engine = WorkflowEngine(
            task_planner=self.planner,
            browser_engine=self.mock_browser,
            desktop_launcher=self.mock_desktop,
            excel_manager=self.mock_excel,
        )

    def test_run_real_electricity_bill_workflow(self):
        self.mock_browser.launch_browser.return_value = True
        self.mock_browser.is_browser_running.return_value = True

        mock_page = MagicMock()
        mock_page.is_closed.return_value = False
        self.mock_browser._page = mock_page

        mock_browser_inst = MagicMock()
        self.mock_browser._browser = mock_browser_inst
        mock_context = MagicMock()
        mock_browser_inst.contexts = [mock_context]
        mock_context.pages = [mock_page]


        # Mock the expects and download info
        mock_download_info = MagicMock()
        mock_download = MagicMock()
        mock_download_info.value = mock_download
        mock_page.expect_download.return_value.__enter__.return_value = mock_download_info

        # Execute
        result = self.engine.execute("Download latest electricity bill")
        self.assertTrue(result)

        # Confirm Playwright mock calls
        self.mock_browser.launch_browser.assert_called_once()
        # open_url should be called for example login, google search, download trigger page, and sample tabs page
        self.assertTrue(self.mock_browser.open_url.call_count >= 2)


if __name__ == "__main__":
    unittest.main()
