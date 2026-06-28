import unittest
from unittest.mock import MagicMock
from src.excel.manager import ExcelManager
from src.excel.analyzer import WorkbookAnalyzer


class TestWorkbookAnalyzer(unittest.TestCase):
    """Test cases for WorkbookAnalyzer."""

    def setUp(self):
        self.mock_excel = MagicMock(spec=ExcelManager)
        # Mock logger on mock_excel
        self.mock_logger = MagicMock()
        self.mock_excel.logger = self.mock_logger
        self.analyzer = WorkbookAnalyzer(self.mock_excel)

    def test_get_workbook_summary_no_wb(self):
        # Setup self.mock_excel.wb to be None
        self.mock_excel.wb = None

        result = self.analyzer.get_workbook_summary()
        self.assertEqual(result, {})
        self.mock_logger.error.assert_called_once_with(
            "Workbook analysis failed: No active workbook loaded."
        )

    def test_get_workbook_summary_success(self):
        # Setup mock workbook and sheets
        mock_wb = MagicMock()
        self.mock_excel.wb = mock_wb
        self.mock_excel.current_path = "D:/path/to/test_file.xlsx"

        self.mock_excel.get_sheet_names.return_value = ["Sheet1", "Sheet2"]
        self.mock_excel.get_active_sheet_name.return_value = "Sheet1"

        # Mock worksheet objects
        mock_sheet1 = MagicMock()
        mock_sheet1.max_row = 15
        mock_sheet1.max_column = 8

        mock_sheet2 = MagicMock()
        mock_sheet2.max_row = 50
        mock_sheet2.max_column = 2

        # Configure mock_wb to index sheets
        mock_wb.__getitem__.side_effect = lambda name: {
            "Sheet1": mock_sheet1,
            "Sheet2": mock_sheet2,
        }[name]

        result = self.analyzer.get_workbook_summary()

        expected = {
            "workbook_name": "test_file.xlsx",
            "number_of_sheets": 2,
            "sheet_names": ["Sheet1", "Sheet2"],
            "active_sheet": "Sheet1",
            "sheet_dimensions": {
                "Sheet1": {"row_count": 15, "column_count": 8},
                "Sheet2": {"row_count": 50, "column_count": 2},
            },
        }
        self.assertEqual(result, expected)
        self.mock_logger.info.assert_any_call("Workbook analysis completed successfully.")

    def test_get_workbook_summary_exception(self):
        mock_wb = MagicMock()
        self.mock_excel.wb = mock_wb
        self.mock_excel.get_sheet_names.side_effect = Exception("Internal Error")

        result = self.analyzer.get_workbook_summary()
        self.assertEqual(result, {})
        self.mock_logger.error.assert_called_once()


if __name__ == "__main__":
    unittest.main()
