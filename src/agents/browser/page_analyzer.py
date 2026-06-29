"""
RAYZEN AI
Browser Page Analyzer

Version : 0.1.0
"""

from typing import Dict, Any, List
from src.core.logger import RayzenLogger


class PageAnalyzer:
    """Scans and analyzes active page DOM elements, metadata, and structural features."""

    def __init__(self):
        self.logger = RayzenLogger()
        self._input_candidates = [
            "input[type='text']",
            "input[type='email']",
            "input[type='password']",
            "#username",
            "#password",
            "#email",
            "input",
        ]
        self._button_candidates = [
            "button",
            "input[type='submit']",
            "#submit-btn",
            ".btn",
            "a.button",
        ]

    def analyze_page(self, page_control, element_engine) -> Dict[str, Any]:
        """Scans the active browser page to identify metadata and interactive DOM elements.

        Args:
            page_control: PageController instance.
            element_engine: ElementEngine instance.

        Returns:
            Dict[str, Any]: Page analysis structure.
        """
        self.logger.info("Starting page layout structure analysis...")
        analysis = {
            "url": "",
            "title": "",
            "inputs": [],
            "buttons": [],
        }

        try:
            # 1. Retrieve page metadata
            analysis["url"] = page_control.get_current_url() or ""
            analysis["title"] = page_control.get_page_title() or ""

            # 2. Check input elements existence
            for selector in self._input_candidates:
                if element_engine.exists(selector):
                    analysis["inputs"].append(selector)

            # 3. Check button elements existence
            for selector in self._button_candidates:
                if element_engine.exists(selector):
                    analysis["buttons"].append(selector)

            self.logger.info(
                f"Page analysis complete. Inputs found: {len(analysis['inputs'])}, Buttons found: {len(analysis['buttons'])}"
            )

        except Exception as e:
            self.logger.error(f"Error during page structure analysis: {e}")

        return analysis
