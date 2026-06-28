"""
RAYZEN AI
Desktop Launcher

Version : 0.1.0
"""

import subprocess
from src.core.logger import RayzenLogger


class DesktopLauncher:
    """Launch Windows applications."""

    def __init__(self):
        self.logger = RayzenLogger()

    def open_notepad(self) -> bool:
        """Open Notepad."""
        try:
            self.logger.info("Opening Notepad...")
            subprocess.Popen("notepad.exe")
            self.logger.info("Notepad opened successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Failed to open Notepad: {e}")
            return False

    def open_calculator(self) -> bool:
        """Open Calculator."""
        try:
            self.logger.info("Opening Calculator...")
            subprocess.Popen("calc.exe")
            self.logger.info("Calculator opened successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Failed to open Calculator: {e}")
            return False

    def open_explorer(self) -> bool:
        """Open File Explorer."""
        try:
            self.logger.info("Opening File Explorer...")
            subprocess.Popen("explorer.exe")
            self.logger.info("File Explorer opened successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Failed to open File Explorer: {e}")
            return False

    def open_paint(self) -> bool:
        """Open Paint."""
        try:
            self.logger.info("Opening Paint...")
            subprocess.Popen("mspaint.exe")
            self.logger.info("Paint opened successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Failed to open Paint: {e}")
            return False

