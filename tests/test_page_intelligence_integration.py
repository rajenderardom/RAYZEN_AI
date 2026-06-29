"""
RAYZEN AI
Page Intelligence Integration Tests

Version : 0.1.0
"""

import unittest
from unittest.mock import MagicMock
from src.agents.browser.page_analyzer import PageAnalyzer
from src.browser.element_engine import ElementEngine
from src.browser.playwright_engine import PlaywrightEngine
from src.agents.browser.page_intelligence import PageIntelligence, PageAnalysisResult


class TestPageIntelligenceIntegration(unittest.TestCase):
    """Integration tests validating page analyzer data coordination and semantic parsing flow."""

    def setUp(self):
        self.analyzer = PageAnalyzer()
        self.mock_element = MagicMock(spec=ElementEngine)
        self.mock_playwright = MagicMock(spec=PlaywrightEngine)

        self.pi = PageIntelligence(
            page_analyzer=self.analyzer,
            element_engine=self.mock_element,
            playwright_engine=self.mock_playwright,
        )

    def test_end_to_end_analysis_routing(self):
        # Configure playwright engine mocks
        self.mock_playwright.is_browser_running.return_value = True
        mock_page = MagicMock()
        mock_page.url = "https://example.com/search?q=test"
        mock_page.title.return_value = "Query Page"
        self.mock_playwright._page = mock_page

        # Configure element engine mocks
        self.mock_element.exists.side_effect = lambda s: s in ("input", "button", "table")

        # Run analyze pipeline
        result = self.pi.analyze()

        # Validate results matching search heuristics
        self.assertIsInstance(result, PageAnalysisResult)
        self.assertEqual(result.url, "https://example.com/search?q=test")
        self.assertEqual(result.title, "Query Page")
        self.assertEqual(result.page_type, "search")
        self.assertEqual(result.confidence, 0.9)  # 0.5 base + 0.4 input search match
        self.assertIn("input", result.inputs)
        self.assertIn("button", result.buttons)
        self.assertEqual(len(result.tables), 1)
        self.assertEqual(result.tables[0]["selector"], "table")
        self.assertEqual(
            result.recommended_next_action,
            "Enter your query string in the search box and press Enter."
        )


if __name__ == "__main__":
    unittest.main()
