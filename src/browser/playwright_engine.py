"""
RAYZEN AI
Playwright Browser Engine

Version : 0.1.0
"""

from typing import Optional

# Placeholder for lazy import of Playwright sync API.
sync_playwright = None

from src.core.logger import RayzenLogger


class PlaywrightEngine:
    """Manages browser automation using Playwright Chromium."""

    def __init__(self):
        """Initialize the Playwright engine with empty active state."""
        self.logger = RayzenLogger()
        self._playwright: Optional["Playwright"] = None
        self._browser: Optional["Browser"] = None
        self._page: Optional["Page"] = None

    def _ensure_sync_playwright(self):
        """Return a callable sync_playwright, respecting existing mocks.

        If `sync_playwright` is already a callable (including a unittest.mock), use it.
        Otherwise, import it lazily from playwright.sync_api.
        """
        global sync_playwright
        if callable(sync_playwright):
            return sync_playwright
        try:
            from playwright.sync_api import sync_playwright as real_sync_playwright
            sync_playwright = real_sync_playwright
            return sync_playwright
        except Exception as e:
            self.logger.error(f"Failed to import sync_playwright: {e}")
            raise
    def launch_browser(self, headless: bool = False) -> bool:
        """Launch the Chromium browser instance.

        Args:
            headless (bool): Run browser in headless mode. Defaults to False.

        Returns:
            bool: True on success, False on failure.
        """
        if self.is_browser_running():
            self.logger.info("Browser is already running.")
            return True

        try:
            self.logger.info(f"Launching Chromium browser (headless={headless})...")
            # Ensure sync_playwright is available, respecting any existing mock
            sync_playwright_fn = self._ensure_sync_playwright()
            self._playwright = sync_playwright_fn().start()
            self._browser = self._playwright.chromium.launch(headless=headless)
            context = self._browser.new_context()
            self._page = context.new_page()
            self.logger.info("Chromium browser launched successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Failed to launch browser: {e}")
            self.close_browser()
            return False

    def open_url(self, url: str) -> bool:
        """Navigate to the specified URL in the active browser page.

        Args:
            url (str): The target URL.

        Returns:
            bool: True on success, False on failure.
        """
        if not self.is_browser_running():
            self.logger.info("Browser is not running. Launching default instance...")
            if not self.launch_browser():
                self.logger.error("Cannot open URL because browser failed to launch.")
                return False

        try:
            self.logger.info(f"Navigating to: {url}")
            if self._page:
                self._page.goto(url)
                self.logger.info(f"Successfully opened: {url}")
                return True
            else:
                self.logger.error("No active page found to open URL.")
                return False
        except Exception as e:
            self.logger.error(f"Failed to open URL '{url}': {e}")
            return False

    def close_browser(self) -> bool:
        """Close the Chromium browser and stop Playwright.

        Returns:
            bool: True on success, False on failure.
        """
        try:
            self.logger.info("Closing browser and stopping Playwright...")
            if self._page:
                self._page = None
            if self._browser:
                self._browser.close()
                self._browser = None
            if self._playwright:
                self._playwright.stop()
                self._playwright = None
            self.logger.info("Browser closed successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Error occurred while closing browser: {e}")
            return False

    def is_browser_running(self) -> bool:
        """Check if the Chromium browser is active.

        Returns:
            bool: True if running, False otherwise.
        """
        return self._browser is not None and self._browser.is_connected()
