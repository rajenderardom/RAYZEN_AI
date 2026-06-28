"""
RAYZEN AI
Core Application

Version : 0.1.0 Genesis
"""

from src.core.config import AppConfig


class RayzenApp:
    """Main application class for RAYZEN AI."""

    def __init__(self):
        self.config = AppConfig()

    def start(self):
        print("=" * 50)
        print(self.config.app_name)
        print(f"Version : {self.config.version}")
        print(f"Author  : {self.config.author}")
        print(f"Debug   : {self.config.debug}")
        print("=" * 50)
        print("Core Engine Started Successfully.")
        print("=" * 50)
