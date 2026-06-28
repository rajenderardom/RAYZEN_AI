"""
RAYZEN AI
Core Application

Version : 0.1.0 Genesis
"""

from src.core.config import AppConfig
from src.core.logger import RayzenLogger


class RayzenApp:
    """Main application class."""

    def __init__(self):
        self.config = AppConfig()
        self.logger = RayzenLogger()

    def start(self):
        print("=" * 50)
        print(self.config.app_name)
        print(f"Version : {self.config.version}")
        print(f"Author  : {self.config.author}")
        print(f"Debug   : {self.config.debug}")
        print("=" * 50)

        self.logger.info("Core Engine Started Successfully.")

        print("=" * 50)
