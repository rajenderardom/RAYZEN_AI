import unittest
from unittest.mock import MagicMock
from src.brain.intent_analyzer import IntentAnalyzer
from src.brain.task_planner import TaskPlanner


class TestTaskPlanner(unittest.TestCase):
    """Test cases for TaskPlanner."""

    def setUp(self):
        self.mock_analyzer = MagicMock(spec=IntentAnalyzer)
        self.mock_logger = MagicMock()
        self.mock_analyzer.logger = self.mock_logger
        self.planner = TaskPlanner(self.mock_analyzer)

    def test_create_plan_desktop_open(self):
        self.mock_analyzer.analyze.return_value = {
            "intent": "desktop.open",
            "target": "calculator",
            "confidence": 1.0,
        }
        plan = self.planner.create_plan("Open Calculator")
        self.assertEqual(plan, ["Launch Calculator"])

    def test_create_plan_desktop_open_explorer(self):
        self.mock_analyzer.analyze.return_value = {
            "intent": "desktop.open",
            "target": "explorer",
            "confidence": 1.0,
        }
        plan = self.planner.create_plan("open explorer")
        self.assertEqual(plan, ["Launch File Explorer"])

    def test_create_plan_browser_open(self):
        self.mock_analyzer.analyze.return_value = {
            "intent": "browser.open",
            "target": "github",
            "confidence": 1.0,
        }
        plan = self.planner.create_plan("open github")
        self.assertEqual(plan, ["Launch Browser", "Open GitHub"])

    def test_create_plan_excel_analyze(self):
        self.mock_analyzer.analyze.return_value = {
            "intent": "excel.analyze",
            "file": "data.xlsx",
            "confidence": 0.95,
        }
        plan = self.planner.create_plan("analyze data.xlsx")
        self.assertEqual(
            plan,
            [
                "Load Workbook: data.xlsx",
                "Analyze Sheet Structure",
                "Calculate Sheet Dimensions",
            ],
        )

    def test_create_plan_browser_workflow(self):
        self.mock_analyzer.analyze.return_value = {
            "intent": "browser.workflow",
            "task": "download electricity bill",
            "confidence": 0.80,
        }
        plan = self.planner.create_plan("Download latest electricity bill")
        expected = [
            "Launch Browser",
            "Open Website",
            "Login",
            "Navigate",
            "Download File",
            "Verify Download",
        ]
        self.assertEqual(plan, expected)

    def test_create_plan_unknown(self):
        self.mock_analyzer.analyze.return_value = {"intent": "unknown", "confidence": 0.0}
        plan = self.planner.create_plan("run randomized script")
        self.assertEqual(plan, [])

    def test_create_plan_invalid_type(self):
        plan = self.planner.create_plan(None)  # type: ignore
        self.assertEqual(plan, [])


if __name__ == "__main__":
    unittest.main()
