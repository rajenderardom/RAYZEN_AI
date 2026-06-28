"""
RAYZEN AI
Browser Controller

Version : 0.1.0
"""

import webbrowser
from src.core.logger import RayzenLogger


class BrowserController:
    """Controls browser actions on Windows."""

    def __init__(self):
        self.logger = RayzenLogger()

    def open_default_browser(self, url: str) -> bool:
        """Open the default system browser to the specified URL.

        Args:
            url (str): The URL to open.

        Returns:
            bool: True on success, False on failure.
        """
        try:
            self.logger.info(f"Opening browser at URL: {url}")
            success = webbrowser.open(url)
            if success:
                self.logger.info(f"Successfully opened URL: {url}")
                return True
            else:
                self.logger.error(f"Failed to open URL: {url}")
                return False
        except Exception as e:
            self.logger.error(f"Exception occurred while opening URL '{url}': {e}")
            return False

    def open_google(self) -> bool:
        """Open Google in the default browser.

        Returns:
            bool: True on success, False on failure.
        """
        return self.open_default_browser("https://www.google.com")

    def open_github(self) -> bool:
        """Open GitHub in the default browser.

        Returns:
            bool: True on success, False on failure.
        """
        return self.open_default_browser("https://github.com")

    def open_chatgpt(self) -> bool:
        """Open ChatGPT in the default browser.

        Returns:
            bool: True on success, False on failure.
        """
        return self.open_default_browser("https://chatgpt.com")
