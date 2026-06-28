"""
RAYZEN AI
Core Application

Version : 0.1.0 Genesis
"""

from src.core.config import AppConfig
from src.core.logger import RayzenLogger
from src.core.settings import SettingsManager
from src.desktop.launcher import DesktopLauncher
from src.browser.controller import BrowserController
from src.core.command_engine import CommandEngine


class RayzenApp:
    """Main application class."""

    def __init__(self):
        self.config = AppConfig()
        self.logger = RayzenLogger()
        self.settings = SettingsManager()
        self.desktop = DesktopLauncher()
        self.browser = BrowserController()
        self.command_engine = CommandEngine(self.desktop, self.browser, self.logger)

    def start(self):
        """Start the interactive console command loop."""
        print("=" * 40)
        print("RAYZEN AI v0.2")
        print("Type 'help' to view commands.")
        print("Type 'exit' to quit.")
        print("=" * 40)

        self.logger.info("Core Engine Started Successfully.")

        while True:
            try:
                command = input("> ")
            except (KeyboardInterrupt, EOFError):
                break

            normalized = command.strip().lower()
            if not normalized:
                continue

            if normalized == "exit":
                break
            elif normalized == "help":
                self.show_help()
            elif normalized in self.command_engine.get_available_commands():
                self.command_engine.execute(command)
            else:
                # Triggers the CommandEngine warning and prints message to stdout
                self.command_engine.execute(command)
                print("Unknown command.")

    def show_help(self):
        """Display help information and supported commands."""
        print("Supported commands:")
        for cmd in self.command_engine.get_available_commands():
            print(f"- {cmd}")
        print("- help")
        print("- exit")


