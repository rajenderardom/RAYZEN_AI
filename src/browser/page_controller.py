"""
RAYZEN AI
Browser Page Controller

Version : 0.1.0
"""

from typing import List, Optional
from playwright.sync_api import BrowserContext
from src.browser.playwright_engine import PlaywrightEngine
from src.core.logger import RayzenLogger


class PageController:
    """Controls individual pages and tabs in the browser."""

    def __init__(self, playwright_engine: PlaywrightEngine):
        """Initialize PageController.

        Args:
            playwright_engine (PlaywrightEngine): Playwright engine instance.
        """
        self.engine = playwright_engine
        self.logger = RayzenLogger()


    @property
    def current_context(self) -> Optional[BrowserContext]:
        """Retrieve the current active browser context.

        Returns:
            Optional[BrowserContext]: Context instance if running, None otherwise.
        """
        if not self.engine._browser:
            return None
        contexts = self.engine._browser.contexts
        return contexts[0] if contexts else None

    def new_tab(self) -> bool:
        """Create a new tab (page) in the active browser context.

        Returns:
            bool: True on success, False on failure.
        """
        if not self.engine.is_browser_running():
            self.logger.error("Cannot create new tab: Browser is not running.")
            return False
        try:
            self.logger.info("Creating new tab.")
            context = self.current_context
            if not context:
                self.logger.error("No active browser context found.")
                return False
            new_page = context.new_page()
            # Update active page pointer in PlaywrightEngine
            self.engine._page = new_page
            self.logger.info("New tab created and selected.")
            return True
        except Exception as e:
            self.logger.error(f"Failed to create new tab: {e}")
            return False

    def close_current_tab(self) -> bool:
        """Close the currently selected tab.

        Returns:
            bool: True on success, False on failure.
        """
        if not self.engine.is_browser_running() or not self.engine._page:
            self.logger.error("Cannot close tab: No active browser page running.")
            return False
        try:
            self.logger.info("Closing current tab.")
            context = self.current_context
            if not context:
                return False

            current_page = self.engine._page
            current_page.close()

            # Select another active tab if available
            remaining_pages = [p for p in context.pages if not p.is_closed()]
            if remaining_pages:
                self.engine._page = remaining_pages[-1]
            else:
                self.engine._page = None

            self.logger.info("Current tab closed.")
            return True
        except Exception as e:
            self.logger.error(f"Failed to close current tab: {e}")
            return False

    def switch_to_tab(self, index: int) -> bool:
        """Switch the active page reference to the tab at the given index.

        Args:
            index (int): 0-based index of the target tab.

        Returns:
            bool: True on success, False on failure.
        """
        if not self.engine.is_browser_running():
            self.logger.error("Cannot switch tab: Browser is not running.")
            return False
        try:
            self.logger.info(f"Switching to tab index: {index}")
            context = self.current_context
            if not context:
                return False
            pages = context.pages
            if 0 <= index < len(pages):
                self.engine._page = pages[index]
                self.logger.info(f"Switched to tab URL: {pages[index].url}")
                return True
            else:
                self.logger.error(
                    f"Tab index {index} out of range. Total tabs: {len(pages)}"
                )
                return False
        except Exception as e:
            self.logger.error(f"Failed to switch tab: {e}")
            return False

    def refresh_page(self) -> bool:
        """Reload/refresh the current page.

        Returns:
            bool: True on success, False on failure.
        """
        if not self.engine.is_browser_running() or not self.engine._page:
            self.logger.error("Cannot refresh page: No active page running.")
            return False
        try:
            self.logger.info("Refreshing current page.")
            self.engine._page.reload()
            return True
        except Exception as e:
            self.logger.error(f"Failed to refresh page: {e}")
            return False

    def go_back(self) -> bool:
        """Navigate to the previous page in history.

        Returns:
            bool: True on success, False on failure.
        """
        if not self.engine.is_browser_running() or not self.engine._page:
            self.logger.error("Cannot navigate back: No active page running.")
            return False
        try:
            self.logger.info("Navigating back.")
            self.engine._page.go_back()
            return True
        except Exception as e:
            self.logger.error(f"Failed to navigate back: {e}")
            return False

    def go_forward(self) -> bool:
        """Navigate to the next page in history.

        Returns:
            bool: True on success, False on failure.
        """
        if not self.engine.is_browser_running() or not self.engine._page:
            self.logger.error("Cannot navigate forward: No active page running.")
            return False
        try:
            self.logger.info("Navigating forward.")
            self.engine._page.go_forward()
            return True
        except Exception as e:
            self.logger.error(f"Failed to navigate forward: {e}")
            return False

    def get_current_url(self) -> str:
        """Get the URL of the current active page.

        Returns:
            str: The page URL, or empty string if no active page is running.
        """
        if not self.engine.is_browser_running() or not self.engine._page:
            self.logger.error("Cannot get URL: No active page running.")
            return ""
        try:
            url = self.engine._page.url
            self.logger.info(f"Retrieved current URL: {url}")
            return url
        except Exception as e:
            self.logger.error(f"Failed to get current URL: {e}")
            return ""

    def get_page_title(self) -> str:
        """Get the title of the current active page.

        Returns:
            str: The page title, or empty string if no active page is running.
        """
        if not self.engine.is_browser_running() or not self.engine._page:
            self.logger.error("Cannot get title: No active page running.")
            return ""
        try:
            title = self.engine._page.title()
            self.logger.info(f"Retrieved current title: '{title}'")
            return title
        except Exception as e:
            self.logger.error(f"Failed to get page title: {e}")
            return ""

    def list_open_tabs(self) -> List[str]:
        """List the URLs of all open tabs in the current context.

        Returns:
            List[str]: A list of URLs of open tabs.
        """
        if not self.engine.is_browser_running():
            self.logger.error("Cannot list tabs: Browser is not running.")
            return []
        try:
            context = self.current_context
            if not context:
                return []
            urls = [page.url for page in context.pages]
            self.logger.info(f"Retrieved active tabs URLs list: {urls}")
            return urls
        except Exception as e:
            self.logger.error(f"Failed to list open tabs: {e}")
            return []
