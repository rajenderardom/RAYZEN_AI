"""
RAYZEN AI
Excel Manager

Version : 0.1.0
"""

from typing import List, Optional
import openpyxl
from src.core.logger import RayzenLogger


class ExcelManager:
    """Manages Excel file operations using openpyxl."""

    def __init__(self):
        """Initialize ExcelManager with a logger and empty workbook state."""
        self.logger = RayzenLogger()
        self.wb: Optional[openpyxl.Workbook] = None
        self.current_path: Optional[str] = None

    def open_workbook(self, path: str) -> bool:
        """Open an Excel workbook at the specified path.

        Args:
            path (str): Path to the Excel workbook file.

        Returns:
            bool: True on success, False on failure.
        """
        try:
            self.logger.info(f"Opening workbook: {path}")
            self.wb = openpyxl.load_workbook(path)
            self.current_path = path
            self.logger.info(f"Workbook opened successfully: {path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to open workbook '{path}': {e}")
            self.wb = None
            self.current_path = None
            return False

    def save_workbook(self) -> bool:
        """Save the currently open workbook.

        Returns:
            bool: True on success, False on failure.
        """
        if not self.wb or not self.current_path:
            self.logger.error("No active workbook loaded to save.")
            return False
        try:
            self.logger.info(f"Saving workbook to: {self.current_path}")
            self.wb.save(self.current_path)
            self.logger.info("Workbook saved successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save workbook to '{self.current_path}': {e}")
            return False

    def close_workbook(self) -> bool:
        """Close the currently open workbook.

        Returns:
            bool: True on success, False on failure.
        """
        if not self.wb:
            self.logger.info("No active workbook loaded to close.")
            return True
        try:
            self.logger.info("Closing workbook.")
            self.wb.close()
            self.wb = None
            self.current_path = None
            self.logger.info("Workbook closed successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Failed to close workbook: {e}")
            return False

    def get_sheet_names(self) -> List[str]:
        """Get names of all sheets in the workbook.

        Returns:
            List[str]: List of sheet names, or empty list if no workbook is open.
        """
        if not self.wb:
            self.logger.error("No workbook open. Cannot get sheet names.")
            return []
        try:
            sheets = self.wb.sheetnames
            self.logger.info(f"Retrieved sheet names: {sheets}")
            return list(sheets)
        except Exception as e:
            self.logger.error(f"Failed to get sheet names: {e}")
            return []

    def get_active_sheet_name(self) -> str:
        """Get the name of the active sheet.

        Returns:
            str: Name of the active sheet, or empty string if no workbook is open.
        """
        if not self.wb:
            self.logger.error("No workbook open. Cannot get active sheet name.")
            return ""
        try:
            active_sheet = self.wb.active
            name = active_sheet.title if active_sheet else ""
            self.logger.info(f"Retrieved active sheet name: '{name}'")
            return name
        except Exception as e:
            self.logger.error(f"Failed to get active sheet name: {e}")
            return ""
