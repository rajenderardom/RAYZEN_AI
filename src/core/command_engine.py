"""
RAYZEN AI
Command Engine

Version : 0.1.0
"""

from typing import Dict, Callable, List
from src.core.logger import RayzenLogger
from src.desktop.launcher import DesktopLauncher
from src.browser.controller import BrowserController


class CommandEngine:
    """Routes text commands to application launcher and browser controller modules."""

    def __init__(
        self,
        desktop_launcher: DesktopLauncher,
        browser_controller: BrowserController,
        logger: RayzenLogger,
    ):
        """Initialize the command engine with dependencies and command mapping.

        Args:
            desktop_launcher (DesktopLauncher): Launcher for desktop apps.
            browser_controller (BrowserController): Controller for default browser.
            logger (RayzenLogger): Application logger instance.
        """
        self.desktop = desktop_launcher
        self.browser = browser_controller
        self.logger = logger

        # Registry pattern instead of long if-else chains for high extensibility.
        self._commands: Dict[str, Callable[[], bool]] = {
            "open notepad": self.desktop.open_notepad,
            "open calculator": self.desktop.open_calculator,
            "open explorer": self.desktop.open_explorer,
            "open paint": self.desktop.open_paint,
            "open google": self.browser.open_google,
            "open github": self.browser.open_github,
            "open chatgpt": self.browser.open_chatgpt,
        }

    def get_available_commands(self) -> List[str]:
        """Get the list of all registered commands.

        Returns:
            List[str]: A list of command strings.
        """
        return sorted(self._commands.keys())

    def execute(self, command: str) -> bool:
        """Execute a text command by finding and running its mapped handler.

        Args:
            command (str): The command to execute.

        Returns:
            bool: True on success, False on failure.
        """
        if not isinstance(command, str):
            self.logger.error("Command execution failed: Command must be a string.")
            return False

        normalized_command = command.strip().lower()
        handler = self._commands.get(normalized_command)

        if handler:
            self.logger.info(f"Command Engine executing command: '{normalized_command}'")
            try:
                return handler()
            except Exception as e:
                self.logger.error(
                    f"Exception raised while executing command '{normalized_command}': {e}"
                )
                return False
        else:
            # Logs a warning warning using the underlying logger
            self.logger.logger.warning(f"Unknown command: '{command}'")
            return False

