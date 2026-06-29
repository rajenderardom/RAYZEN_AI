"""
RAYZEN AI
Browser Element Engine

Version : 0.1.0
"""

from src.browser.playwright_engine import PlaywrightEngine
from src.core.logger import RayzenLogger


class ElementEngine:
    """Handles page element interactions using Playwright."""

    def __init__(self, playwright_engine: PlaywrightEngine):
        """Initialize ElementEngine.

        Args:
            playwright_engine (PlaywrightEngine): Playwright engine instance.
        """
        self.engine = playwright_engine
        self.logger = RayzenLogger()


    def _get_active_page(self):
        """Check browser state and get active page.

        Raises:
            RuntimeError: If browser or active page is not initialized.
        """
        if not self.engine.is_browser_running() or not self.engine._page:
            raise RuntimeError("Browser is not running or no active page found.")
        return self.engine._page

    def click(self, selector: str) -> bool:
        """Click on the element matching the selector.

        Args:
            selector (str): Element selector.

        Returns:
            bool: True on success, False on failure.
        """
        try:
            page = self._get_active_page()
            self.logger.info(f"Clicking element: '{selector}'")
            page.click(selector)
            return True
        except Exception as e:
            self.logger.error(f"Failed to click element '{selector}': {e}")
            return False

    def type_text(self, selector: str, text: str) -> bool:
        """Type text into the element matching the selector.

        Args:
            selector (str): Input element selector.
            text (str): Text to enter.

        Returns:
            bool: True on success, False on failure.
        """
        try:
            page = self._get_active_page()
            self.logger.info(f"Typing text into element '{selector}'")
            page.fill(selector, text)
            return True
        except Exception as e:
            self.logger.error(f"Failed to type text in element '{selector}': {e}")
            return False

    def clear(self, selector: str) -> bool:
        """Clear the text content of the input element matching the selector.

        Args:
            selector (str): Input element selector.

        Returns:
            bool: True on success, False on failure.
        """
        try:
            page = self._get_active_page()
            self.logger.info(f"Clearing element '{selector}'")
            page.fill(selector, "")
            return True
        except Exception as e:
            self.logger.error(f"Failed to clear element '{selector}': {e}")
            return False

    def press_key(self, key: str) -> bool:
        """Simulate pressing a specific key on the page keyboard.

        Args:
            key (str): Key name (e.g. 'Enter', 'Tab').

        Returns:
            bool: True on success, False on failure.
        """
        try:
            page = self._get_active_page()
            self.logger.info(f"Pressing key: '{key}'")
            page.keyboard.press(key)
            return True
        except Exception as e:
            self.logger.error(f"Failed to press key '{key}': {e}")
            return False

    def hover(self, selector: str) -> bool:
        """Hover over the element matching the selector.

        Args:
            selector (str): Element selector.

        Returns:
            bool: True on success, False on failure.
        """
        try:
            page = self._get_active_page()
            self.logger.info(f"Hovering over element: '{selector}'")
            page.hover(selector)
            return True
        except Exception as e:
            self.logger.error(f"Failed to hover over element '{selector}': {e}")
            return False

    def scroll_to(self, selector: str) -> bool:
        """Scroll the element matching the selector into view.

        Args:
            selector (str): Element selector.

        Returns:
            bool: True on success, False on failure.
        """
        try:
            page = self._get_active_page()
            self.logger.info(f"Scrolling to element: '{selector}'")
            page.locator(selector).scroll_into_view_if_needed()
            return True
        except Exception as e:
            self.logger.error(f"Failed to scroll to element '{selector}': {e}")
            return False

    def wait_for(self, selector: str, timeout: int = 10000) -> bool:
        """Wait for the element matching the selector to appear.

        Args:
            selector (str): Element selector.
            timeout (int): Timeout in milliseconds. Defaults to 10000.

        Returns:
            bool: True on success, False on failure.
        """
        try:
            page = self._get_active_page()
            self.logger.info(f"Waiting for selector: '{selector}' (timeout={timeout}ms)")
            page.wait_for_selector(selector, timeout=timeout)
            return True
        except Exception as e:
            self.logger.error(f"Failed waiting for selector '{selector}': {e}")
            return False

    def get_text(self, selector: str) -> str:
        """Get inner text of the element matching the selector.

        Args:
            selector (str): Element selector.

        Returns:
            str: Inner text, or empty string on failure.
        """
        try:
            page = self._get_active_page()
            self.logger.info(f"Retrieving inner text for: '{selector}'")
            text = page.locator(selector).inner_text()
            return text
        except Exception as e:
            self.logger.error(f"Failed to get text for '{selector}': {e}")
            return ""

    def get_html(self, selector: str) -> str:
        """Get inner HTML of the element matching the selector.

        Args:
            selector (str): Element selector.

        Returns:
            str: Inner HTML content, or empty string on failure.
        """
        try:
            page = self._get_active_page()
            self.logger.info(f"Retrieving inner HTML for: '{selector}'")
            html = page.locator(selector).inner_html()
            return html
        except Exception as e:
            self.logger.error(f"Failed to get HTML for '{selector}': {e}")
            return ""

    def exists(self, selector: str) -> bool:
        """Check if an element matching the selector is present on the page.

        Args:
            selector (str): Element selector.

        Returns:
            bool: True if element exists, False otherwise.
        """
        try:
            page = self._get_active_page()
            count = page.locator(selector).count()
            exists_status = count > 0
            self.logger.info(f"Element existence check for '{selector}': {exists_status}")
            return exists_status
        except Exception as e:
            self.logger.error(f"Error checking existence for '{selector}': {e}")
            return False
