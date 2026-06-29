import unittest
from unittest.mock import patch, MagicMock
from src.core.app import RayzenApp


class TestSystemIntegration(unittest.TestCase):
    """Smoke and integration tests verifying final system wiring."""

    def setUp(self):
        self.app = RayzenApp()

    def test_wiring_completeness(self):
        # Verify all skills are registered
        skills = self.app.skill_registry.list_skills()
        expected = [
            "browser_controller",
            "desktop",
            "element_engine",
            "excel_analyzer",
            "excel_comparator",
            "excel_duplicate_detector",
            "excel_manager",
            "page_controller",
            "playwright_engine",
            "session_manager",
            "workflow_loader",
            "workflow_runner",
        ]
        self.assertEqual(skills, expected)

    @patch("src.desktop.launcher.DesktopLauncher.open_calculator")
    def test_routing_legacy_command(self, mock_calc):
        mock_calc.return_value = True
        result = self.app.command_engine.execute("open calculator")
        self.assertTrue(result)
        mock_calc.assert_called_once()

    @patch("src.excel.manager.ExcelManager.open_workbook")
    @patch("src.excel.analyzer.WorkbookAnalyzer.get_workbook_summary")
    def test_routing_workflow_engine_excel(self, mock_summary, mock_open):
        mock_open.return_value = True
        mock_summary.return_value = {"sheet_names": ["Sheet1"]}

        # Trigger Excel analysis query which is handled by the new WorkflowEngine
        success = self.app.workflow_engine.execute("analyze data/reports.xlsx")
        self.assertTrue(success)
        mock_open.assert_called_once_with("data/reports.xlsx")
        mock_summary.assert_called_once()


if __name__ == "__main__":
    unittest.main()
