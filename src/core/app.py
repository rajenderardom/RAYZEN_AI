"""
RAYZEN AI
Core Application

Version : 0.1.0 Genesis
"""

from src.core.config import AppConfig
from src.core.logger import RayzenLogger
from src.core.settings import SettingsManager
from src.desktop.launcher import DesktopLauncher


class RayzenApp:
    """Main application class."""

    def __init__(self):
        self.config = AppConfig()
        self.logger = RayzenLogger()
        self.settings = SettingsManager()
        self.desktop = DesktopLauncher()

    def start(self):
        print("=" * 50)
        print(self.config.app_name)
        print(f"Version : {self.config.version}")
        print(f"Author  : {self.config.author}")
        print(f"Theme   : {self.settings.get('theme')}")
        print(f"Language: {self.settings.get('language')}")
        print(f"Debug   : {self.settings.get('debug')}")
        print("=" * 50)

        self.logger.info("Core Engine Started Successfully.")

        print("Opening Notepad...")

        if self.desktop.open_notepad():
            self.logger.info("Notepad Opened Successfully.")

        print("=" * 50)
