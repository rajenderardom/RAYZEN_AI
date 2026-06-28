"""
RAYZEN AI
Excel Workbook Analyzer

Version : 0.1.0
"""

import os
from src.excel.manager import ExcelManager


class WorkbookAnalyzer:
    """Provides analytical summaries of Excel workbooks using ExcelManager."""

    def __init__(self, excel_manager: ExcelManager):
        """Initialize WorkbookAnalyzer with an ExcelManager dependency.

        Args:
            excel_manager (ExcelManager): Excel manager instance.
        """
        self.excel = excel_manager
        self.logger = excel_manager.logger

    def get_workbook_summary(self) -> dict:
        """Analyze the open workbook and compile metadata and sheet dimensions.

        Returns:
            dict: Summary details of sheets and sizes, or empty dict if no active workbook.
        """
        if not self.excel.wb:
            self.logger.error("Workbook analysis failed: No active workbook loaded.")
            return {}

        try:
            self.logger.info("Initializing workbook analysis.")
            wb_name = (
                os.path.basename(self.excel.current_path) if self.excel.current_path else ""
            )
            sheet_names = self.excel.get_sheet_names()
            active_sheet = self.excel.get_active_sheet_name()

            sheet_dimensions = {}
            for name in sheet_names:
                sheet = self.excel.wb[name]
                sheet_dimensions[name] = {
                    "row_count": sheet.max_row,
                    "column_count": sheet.max_column,
                }

            summary = {
                "workbook_name": wb_name,
                "number_of_sheets": len(sheet_names),
                "sheet_names": sheet_names,
                "active_sheet": active_sheet,
                "sheet_dimensions": sheet_dimensions,
            }
            self.logger.info("Workbook analysis completed successfully.")
            return summary
        except Exception as e:
            self.logger.error(f"Error occurred during workbook analysis: {e}")
            return {}
