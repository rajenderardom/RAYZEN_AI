import unittest
from unittest.mock import MagicMock
from src.excel.manager import ExcelManager
from src.excel.analyzer import WorkbookAnalyzer
from src.excel.duplicate_detector import DuplicateDetector


class TestDuplicateDetector(unittest.TestCase):
    """Test cases for DuplicateDetector."""

    def setUp(self):
        self.mock_excel = MagicMock(spec=ExcelManager)
        self.mock_analyzer = MagicMock(spec=WorkbookAnalyzer)
        self.mock_logger = MagicMock()
        self.mock_excel.logger = self.mock_logger
        self.detector = DuplicateDetector(self.mock_excel, self.mock_analyzer)

    def test_find_duplicates_no_workbook(self):
        self.mock_analyzer.get_workbook_summary.return_value = {}

        result = self.detector.find_duplicates("Sheet1", "Email")
        self.assertEqual(result, {})
        self.mock_logger.error.assert_called_once_with(
            "Duplicate detection failed: No active workbook loaded."
        )

    def test_find_duplicates_sheet_not_found(self):
        self.mock_analyzer.get_workbook_summary.return_value = {"sheet_names": ["Sheet2"]}

        result = self.detector.find_duplicates("Sheet1", "Email")
        self.assertEqual(result, {})
        self.mock_logger.error.assert_called_once_with(
            "Duplicate detection failed: Sheet 'Sheet1' not found."
        )

    def test_find_duplicates_column_not_found(self):
        self.mock_analyzer.get_workbook_summary.return_value = {"sheet_names": ["Sheet1"]}
        mock_sheet = MagicMock()
        mock_sheet.max_column = 2

        mock_cell_col1 = MagicMock()
        mock_cell_col1.value = "ID"
        mock_cell_col2 = MagicMock()
        mock_cell_col2.value = "Name"

        mock_sheet.cell.side_effect = lambda row, column: {
            (1, 1): mock_cell_col1,
            (1, 2): mock_cell_col2,
        }.get((row, column))

        mock_wb = MagicMock()
        mock_wb.__getitem__.return_value = mock_sheet
        self.mock_excel.wb = mock_wb

        result = self.detector.find_duplicates("Sheet1", "Email")
        self.assertEqual(result, {})
        self.mock_logger.error.assert_called_once_with(
            "Duplicate detection failed: Column 'Email' not found in sheet 'Sheet1'."
        )

    def test_find_duplicates_success(self):
        self.mock_analyzer.get_workbook_summary.return_value = {"sheet_names": ["Sheet1"]}
        mock_sheet = MagicMock()
        mock_sheet.max_column = 2
        mock_sheet.max_row = 5

        c_1_1 = MagicMock(value="ID")
        c_1_2 = MagicMock(value="Email")

        c_2_1 = MagicMock(value=1)
        c_2_2 = MagicMock(value="test@example.com")

        c_3_1 = MagicMock(value=2)
        c_3_2 = MagicMock(value="test@example.com")

        c_4_1 = MagicMock(value=3)
        c_4_2 = MagicMock(value="unique@example.com")

        c_5_1 = MagicMock(value=4)
        c_5_2 = MagicMock(value="test@example.com")

        cells = {
            (1, 1): c_1_1,
            (1, 2): c_1_2,
            (2, 1): c_2_1,
            (2, 2): c_2_2,
            (3, 1): c_3_1,
            (3, 2): c_3_2,
            (4, 1): c_4_1,
            (4, 2): c_4_2,
            (5, 1): c_5_1,
            (5, 2): c_5_2,
        }

        mock_sheet.cell.side_effect = lambda row, column: cells.get((row, column))

        mock_wb = MagicMock()
        mock_wb.__getitem__.return_value = mock_sheet
        self.mock_excel.wb = mock_wb

        result = self.detector.find_duplicates("Sheet1", "Email")

        expected = {
            "duplicate_values": ["test@example.com"],
            "duplicate_count": 3,
            "row_numbers": {"test@example.com": [2, 3, 5]},
            "sheet_name": "Sheet1",
            "column_name": "Email",
        }
        self.assertEqual(result, expected)

    def test_find_duplicates_exception(self):
        self.mock_analyzer.get_workbook_summary.return_value = {"sheet_names": ["Sheet1"]}
        self.mock_excel.wb = Exception("Failed index mock")

        result = self.detector.find_duplicates("Sheet1", "Email")
        self.assertEqual(result, {})
        self.mock_logger.error.assert_called_once()


if __name__ == "__main__":
    unittest.main()
