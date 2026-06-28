import unittest
from unittest.mock import patch, MagicMock
from src.excel.manager import ExcelManager


class TestExcelManager(unittest.TestCase):
    """Test cases for ExcelManager."""

    def setUp(self):
        self.manager = ExcelManager()

    @patch("openpyxl.load_workbook")
    def test_open_workbook_success(self, mock_load):
        mock_wb = MagicMock()
        mock_load.return_value = mock_wb

        result = self.manager.open_workbook("dummy.xlsx")
        self.assertTrue(result)
        self.assertEqual(self.manager.wb, mock_wb)
        self.assertEqual(self.manager.current_path, "dummy.xlsx")
        mock_load.assert_called_once_with("dummy.xlsx")

    @patch("openpyxl.load_workbook")
    def test_open_workbook_failure(self, mock_load):
        mock_load.side_effect = Exception("File not found")

        result = self.manager.open_workbook("dummy.xlsx")
        self.assertFalse(result)
        self.assertIsNone(self.manager.wb)
        self.assertIsNone(self.manager.current_path)

    def test_save_workbook_no_active_wb(self):
        result = self.manager.save_workbook()
        self.assertFalse(result)

    @patch("openpyxl.load_workbook")
    def test_save_workbook_success(self, mock_load):
        mock_wb = MagicMock()
        mock_load.return_value = mock_wb
        self.manager.open_workbook("dummy.xlsx")

        result = self.manager.save_workbook()
        self.assertTrue(result)
        mock_wb.save.assert_called_once_with("dummy.xlsx")

    @patch("openpyxl.load_workbook")
    def test_save_workbook_failure(self, mock_load):
        mock_wb = MagicMock()
        mock_wb.save.side_effect = Exception("Permission denied")
        mock_load.return_value = mock_wb
        self.manager.open_workbook("dummy.xlsx")

        result = self.manager.save_workbook()
        self.assertFalse(result)

    def test_close_workbook_no_active_wb(self):
        result = self.manager.close_workbook()
        self.assertTrue(result)

    @patch("openpyxl.load_workbook")
    def test_close_workbook_success(self, mock_load):
        mock_wb = MagicMock()
        mock_load.return_value = mock_wb
        self.manager.open_workbook("dummy.xlsx")

        result = self.manager.close_workbook()
        self.assertTrue(result)
        mock_wb.close.assert_called_once()
        self.assertIsNone(self.manager.wb)
        self.assertIsNone(self.manager.current_path)

    def test_get_sheet_names_no_active_wb(self):
        self.assertEqual(self.manager.get_sheet_names(), [])

    @patch("openpyxl.load_workbook")
    def test_get_sheet_names_success(self, mock_load):
        mock_wb = MagicMock()
        mock_wb.sheetnames = ["Sheet1", "Sheet2"]
        mock_load.return_value = mock_wb
        self.manager.open_workbook("dummy.xlsx")

        self.assertEqual(self.manager.get_sheet_names(), ["Sheet1", "Sheet2"])

    def test_get_active_sheet_name_no_active_wb(self):
        self.assertEqual(self.manager.get_active_sheet_name(), "")

    @patch("openpyxl.load_workbook")
    def test_get_active_sheet_name_success(self, mock_load):
        mock_wb = MagicMock()
        mock_sheet = MagicMock()
        mock_sheet.title = "Sheet1"
        mock_wb.active = mock_sheet
        mock_load.return_value = mock_wb
        self.manager.open_workbook("dummy.xlsx")

        self.assertEqual(self.manager.get_active_sheet_name(), "Sheet1")


if __name__ == "__main__":
    unittest.main()
