"""
RAYZEN AI
Excel Duplicate Detector

Version : 0.1.0
"""

from typing import Dict, List, Any
from src.excel.manager import ExcelManager
from src.excel.analyzer import WorkbookAnalyzer


class DuplicateDetector:
    """Detects duplicate row values in worksheets without modifying data."""

    def __init__(self, excel_manager: ExcelManager, workbook_analyzer: WorkbookAnalyzer):
        """Initialize DuplicateDetector.

        Args:
            excel_manager (ExcelManager): Excel manager instance.
            workbook_analyzer (WorkbookAnalyzer): Workbook analyzer instance.
        """
        self.excel = excel_manager
        self.analyzer = workbook_analyzer
        self.logger = excel_manager.logger

    def find_duplicates(self, sheet_name: str, column_name: str) -> dict:
        """Find duplicate values in a specific sheet column.

        Args:
            sheet_name (str): Name of the worksheet.
            column_name (str): Name of the column header to search duplicates in.

        Returns:
            dict: Summary of duplicates, containing values, counts, row numbers, and names.
        """
        # Validate workbook and sheet existence using WorkbookAnalyzer
        summary = self.analyzer.get_workbook_summary()
        if not summary:
            self.logger.error("Duplicate detection failed: No active workbook loaded.")
            return {}

        sheet_names = summary.get("sheet_names", [])
        if sheet_name not in sheet_names:
            self.logger.error(f"Duplicate detection failed: Sheet '{sheet_name}' not found.")
            return {}

        try:
            self.logger.info(
                f"Scanning sheet '{sheet_name}' for duplicates in column '{column_name}'."
            )
            sheet = self.excel.wb[sheet_name]

            # Find column index from header row
            col_index = None
            for col in range(1, sheet.max_column + 1):
                cell_val = sheet.cell(row=1, column=col).value
                if cell_val is not None and str(cell_val).strip() == column_name.strip():
                    col_index = col
                    break

            if col_index is None:
                self.logger.error(
                    f"Duplicate detection failed: Column '{column_name}' not found in sheet '{sheet_name}'."
                )
                return {}

            # Gather occurrences (row index starts at 2 to skip the header)
            occurrences: Dict[Any, List[int]] = {}
            for row in range(2, sheet.max_row + 1):
                val = sheet.cell(row=row, column=col_index).value
                if val is not None:
                    if val not in occurrences:
                        occurrences[val] = []
                    occurrences[val].append(row)

            # Filter for duplicates
            duplicate_values = []
            row_numbers = {}
            duplicate_count = 0

            for val, rows in occurrences.items():
                if len(rows) > 1:
                    duplicate_values.append(val)
                    row_numbers[val] = rows
                    # Total duplicate cell instances
                    duplicate_count += len(rows)

            result = {
                "duplicate_values": duplicate_values,
                "duplicate_count": duplicate_count,
                "row_numbers": row_numbers,
                "sheet_name": sheet_name,
                "column_name": column_name,
            }
            self.logger.info(
                f"Duplicate detection completed. Found {len(duplicate_values)} duplicate values "
                f"across {duplicate_count} total rows."
            )
            return result

        except Exception as e:
            self.logger.error(f"Error occurred while searching duplicates: {e}")
            return {}
