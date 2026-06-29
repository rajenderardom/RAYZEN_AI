"""
RAYZEN AI
Browser Session Manager

Version : 0.1.0
"""

import os
from typing import List
from src.browser.playwright_engine import PlaywrightEngine
from src.core.logger import RayzenLogger


class SessionManager:
    """Manages persistent browser profiles and storage states using Playwright contexts."""

    def __init__(self, playwright_engine: PlaywrightEngine):
        """Initialize SessionManager.

        Args:
            playwright_engine (PlaywrightEngine): Playwright engine instance.
        """
        self.engine = playwright_engine
        self.logger = RayzenLogger()
        self.profile_dir = "data/browser_profiles"

        self._active_profile: str = ""
        os.makedirs(self.profile_dir, exist_ok=True)

    def _get_profile_path(self, profile_name: str) -> str:
        """Helper to get absolute profile file path."""
        # Sanitize profile name to prevent directory traversal
        sanitized_name = "".join(c for c in profile_name if c.isalnum() or c in ("-", "_"))
        return os.path.join(self.profile_dir, f"{sanitized_name}.json")

    def create_context(self, profile_name: str) -> bool:
        """Create a new session profile context.

        Saves the current browser state to the named profile.

        Args:
            profile_name (str): Name of the profile.

        Returns:
            bool: True on success, False on failure.
        """
        if not self.engine.is_browser_running():
            self.logger.error("Cannot create context: Browser is not running.")
            return False

        try:
            self.logger.info(f"Creating profile context: '{profile_name}'")
            profile_path = self._get_profile_path(profile_name)

            # Retrieve active context
            contexts = self.engine._browser.contexts
            if not contexts:
                self.logger.error("No active browser contexts found.")
                return False

            contexts[0].storage_state(path=profile_path)
            self._active_profile = profile_name
            self.logger.info(
                f"Successfully created profile: '{profile_name}' at {profile_path}"
            )
            return True
        except Exception as e:
            self.logger.error(f"Failed to create profile context '{profile_name}': {e}")
            return False

    def load_context(self, profile_name: str) -> bool:
        """Load a saved session profile context into the browser.

        Args:
            profile_name (str): Name of the profile.

        Returns:
            bool: True on success, False on failure.
        """
        profile_path = self._get_profile_path(profile_name)
        if not os.path.exists(profile_path):
            self.logger.error(f"Cannot load context: Profile '{profile_name}' does not exist.")
            return False

        if not self.engine.is_browser_running():
            self.logger.info("Browser is not running. Launching default instance...")
            if not self.engine.launch_browser():
                self.logger.error("Cannot load context because browser failed to launch.")
                return False

        try:
            self.logger.info(f"Loading profile context: '{profile_name}'")

            # Close existing contexts and pages to load storage state fresh
            if self.engine._page:
                self.engine._page.close()
                self.engine._page = None

            for context in list(self.engine._browser.contexts):
                context.close()

            # Create new context loading the storage state
            new_context = self.engine._browser.new_context(storage_state=profile_path)
            self.engine._page = new_context.new_page()
            self._active_profile = profile_name

            self.logger.info(f"Successfully loaded profile: '{profile_name}'")
            return True
        except Exception as e:
            self.logger.error(f"Failed to load profile context '{profile_name}': {e}")
            return False

    def save_context(self, profile_name: str) -> bool:
        """Save the current active browser storage state to the specified profile.

        Args:
            profile_name (str): Name of the profile.

        Returns:
            bool: True on success, False on failure.
        """
        return self.create_context(profile_name)

    def clear_context(self) -> bool:
        """Clear current session cookies and storage state by spawning a fresh context.

        Returns:
            bool: True on success, False on failure.
        """
        if not self.engine.is_browser_running():
            self.logger.info("Browser not running. Nothing to clear.")
            return True
        try:
            self.logger.info("Clearing current session context.")
            if self.engine._page:
                self.engine._page.close()
                self.engine._page = None

            for context in list(self.engine._browser.contexts):
                context.close()

            # Spawn a fresh unauthenticated context
            new_context = self.engine._browser.new_context()
            self.engine._page = new_context.new_page()
            self._active_profile = ""

            self.logger.info("Session context cleared successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Failed to clear session context: {e}")
            return False

    def list_profiles(self) -> List[str]:
        """List all available session profile names.

        Returns:
            List[str]: List of profile names.
        """
        try:
            self.logger.info("Listing all browser profiles.")
            profiles = []
            for file in os.listdir(self.profile_dir):
                if file.endswith(".json"):
                    profiles.append(file[:-5])
            self.logger.info(f"Found profiles: {profiles}")
            return profiles
        except Exception as e:
            self.logger.error(f"Failed to list profiles: {e}")
            return []

    def current_profile(self) -> str:
        """Get the name of the currently loaded profile.

        Returns:
            str: Active profile name, or empty string if none.
        """
        return self._active_profile

    def is_logged_in(self) -> bool:
        """Check if any active cookies/sessions exist in the current context.

        Returns:
            bool: True if context contains session cookies, False otherwise.
        """
        if not self.engine.is_browser_running():
            return False
        try:
            contexts = self.engine._browser.contexts
            if not contexts:
                return False
            cookies = contexts[0].cookies()
            logged_in = len(cookies) > 0
            self.logger.info(f"Logged in session check: {logged_in}")
            return logged_in
        except Exception as e:
            self.logger.error(f"Error checking login state: {e}")
            return False
