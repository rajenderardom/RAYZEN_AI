"""
RAYZEN AI
Browser Recovery Engine

Version : 0.1.0
"""

import time
from src.core.logger import RayzenLogger


class RecoveryEngine:
    """Provides fallback strategies such as reloading pages, waiting, or page navigation history go-back."""

    def __init__(self):
        self.logger = RayzenLogger()

    def reload_page(self, page_control) -> bool:
        """Attempts to recover by reloading the current page.

        Args:
            page_control: PageController instance.

        Returns:
            bool: True on success, False on failure.
        """
        self.logger.warning("Recovery: Reloading the current page...")
        try:
            return page_control.refresh_page()
        except Exception as e:
            self.logger.error(f"Recovery: Page reload failed: {e}")
            return False

    def navigate_back(self, page_control) -> bool:
        """Attempts to recover by navigating back in context history.

        Args:
            page_control: PageController instance.

        Returns:
            bool: True on success, False on failure.
        """
        self.logger.warning("Recovery: Navigating back in page history...")
        try:
            return page_control.go_back()
        except Exception as e:
            self.logger.error(f"Recovery: Page navigation go_back failed: {e}")
            return False

    def wait_and_retry(self, duration_ms: int = 3000) -> bool:
        """Attempts to recover by executing a delay before retrying.

        Args:
            duration_ms (int): Sleep duration.

        Returns:
            bool: True.
        """
        self.logger.warning(f"Recovery: Sleeping for {duration_ms}ms to wait for DOM updates...")
        time.sleep(duration_ms / 1000.0)
        return True
