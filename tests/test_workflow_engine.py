import unittest
from unittest.mock import patch, MagicMock
from src.brain.task_planner import TaskPlanner
from src.browser.playwright_engine import PlaywrightEngine
from src.desktop.launcher import DesktopLauncher
from src.excel.manager import ExcelManager
from src.brain.workflow_engine import WorkflowEngine


class TestWorkflowEngine(unittest.TestCase):
    """Test cases for WorkflowEngine."""

    def setUp(self):
        self.mock_planner = MagicMock(spec=TaskPlanner)
        self.mock_browser = MagicMock(spec=PlaywrightEngine)
        self.mock_desktop = MagicMock(spec=DesktopLauncher)
        self.mock_excel = MagicMock(spec=ExcelManager)

        self.mock_logger = MagicMock()
        self.mock_planner.logger = self.mock_logger

        self.engine = WorkflowEngine(
            task_planner=self.mock_planner,
            browser_engine=self.mock_browser,
            desktop_launcher=self.mock_desktop,
            excel_manager=self.mock_excel,
        )

    def test_execute_invalid_type(self):
        result = self.engine.execute(None)  # type: ignore
        self.assertFalse(result)
        self.mock_logger.error.assert_called_once()

    def test_execute_planner_fails(self):
        self.mock_planner.create_plan.return_value = []
        result = self.engine.execute("Open Notepad")
        self.assertFalse(result)
        self.mock_logger.error.assert_called_once()

    def test_execute_calculator_success(self):
        self.mock_planner.create_plan.return_value = ["Launch Calculator"]
        self.mock_desktop.open_calculator.return_value = True

        result = self.engine.execute("Open Calculator")
        self.assertTrue(result)
        self.mock_desktop.open_calculator.assert_called_once()

    def test_execute_calculator_failure(self):
        self.mock_planner.create_plan.return_value = ["Launch Calculator"]
        self.mock_desktop.open_calculator.return_value = False

        result = self.engine.execute("Open Calculator")
        self.assertFalse(result)
        self.mock_desktop.open_calculator.assert_called_once()
        self.mock_logger.error.assert_any_call(
            "Workflow execution halted: Step 'Launch Calculator' failed."
        )

    def test_execute_browser_open_success(self):
        self.mock_planner.create_plan.return_value = ["Launch Browser", "Open GitHub"]
        self.mock_browser.launch_browser.return_value = True
        self.mock_browser.open_url.return_value = True

        result = self.engine.execute("open github")
        self.assertTrue(result)
        self.mock_browser.launch_browser.assert_called_once_with(headless=False)
        self.mock_browser.open_url.assert_called_once_with("https://github.com")

    @patch("src.excel.analyzer.WorkbookAnalyzer")
    def test_execute_excel_analyze_success(self, mock_analyzer_class):
        self.mock_planner.create_plan.return_value = [
            "Load Workbook: data.xlsx",
            "Analyze Sheet Structure",
            "Calculate Sheet Dimensions",
        ]
        self.mock_excel.open_workbook.return_value = True

        mock_analyzer_inst = MagicMock()
        mock_analyzer_class.return_value = mock_analyzer_inst
        mock_analyzer_inst.get_workbook_summary.return_value = {"sheet_names": ["Sheet1"]}

        result = self.engine.execute("analyze data.xlsx")
        self.assertTrue(result)
        self.mock_excel.open_workbook.assert_called_once_with("data.xlsx")
        mock_analyzer_inst.get_workbook_summary.assert_called_once()

    def test_execute_generic_browser_workflow_success(self):
        self.mock_planner.create_plan.return_value = [
            "Launch Browser",
            "Open Website",
            "Login",
            "Navigate",
            "Download File",
            "Verify Download",
        ]
        self.mock_browser.launch_browser.return_value = True

        mock_runner = MagicMock()
        mock_runner.run.return_value = True
        self.engine.runner = mock_runner

        mock_loader = MagicMock()
        mock_loader.load.return_value = {"steps": []}
        self.engine.loader = mock_loader

        result = self.engine.execute("Download latest electricity bill")
        self.assertTrue(result)
        self.mock_browser.launch_browser.assert_called_once()
        self.assertEqual(mock_loader.load.call_count, 4)
        self.assertEqual(mock_runner.run.call_count, 4)


if __name__ == "__main__":
    unittest.main()
