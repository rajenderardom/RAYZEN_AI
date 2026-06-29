"""
RAYZEN AI
Page Intelligence Unit Tests

Version : 0.1.0
"""

import unittest
from unittest.mock import MagicMock
from src.agents.browser.page_analyzer import PageAnalyzer
from src.browser.element_engine import ElementEngine
from src.browser.playwright_engine import PlaywrightEngine
from src.agents.browser.page_intelligence import PageIntelligence, PageAnalysisResult


class TestPageIntelligence(unittest.TestCase):
    """Unit tests for PageIntelligence class mapping logic and detection heuristics."""

    def setUp(self):
        self.mock_analyzer = MagicMock(spec=PageAnalyzer)
        self.mock_element = MagicMock(spec=ElementEngine)
        self.mock_playwright = MagicMock(spec=PlaywrightEngine)

        self.pi = PageIntelligence(
            page_analyzer=self.mock_analyzer,
            element_engine=self.mock_element,
            playwright_engine=self.mock_playwright,
        )

    def test_detect_page_type_login(self):
        # 1. Test URL keyword
        res = self.pi.detect_page_type("https://host.com/auth/login", "Welcome Portal", [])
        self.assertEqual(res, "login")

        # 2. Test Title keyword
        res = self.pi.detect_page_type("https://host.com/main", "SignIn Screen", [])
        self.assertEqual(res, "login")

        # 3. Test Password inputs existence
        res = self.pi.detect_page_type("https://host.com/main", "Welcome", ["#password_field"])
        self.assertEqual(res, "login")

    def test_detect_page_type_search(self):
        res = self.pi.detect_page_type("https://google.com", "Google Search", [])
        self.assertEqual(res, "search")

    def test_detect_page_type_dashboard(self):
        res = self.pi.detect_page_type("https://myagent.ai/dashboard/overview", "Overview Console", [])
        self.assertEqual(res, "dashboard")

    def test_detect_page_type_report(self):
        res = self.pi.detect_page_type("https://myagent.ai/analytics", "Monthly Export Stats", [])
        self.assertEqual(res, "report")

    def test_detect_page_type_form(self):
        res = self.pi.detect_page_type("https://myagent.ai/fill", "Profile Wizard", ["#input1", "#input2"])
        self.assertEqual(res, "form")

    def test_detect_page_type_unknown(self):
        res = self.pi.detect_page_type("https://myagent.ai/general", "Generic Title", [])
        self.assertEqual(res, "unknown")

    def test_detect_forms(self):
        # Case A: Real form tag exists
        self.mock_element.exists.side_effect = lambda s: s in ("form", "input")
        forms = self.pi.detect_forms()
        self.assertEqual(len(forms), 1)
        self.assertEqual(forms[0]["form_selector"], "form")

        # Case B: Div container virtual form fallback
        self.mock_element.exists.side_effect = lambda s: s in ("input")
        forms = self.pi.detect_forms()
        self.assertEqual(len(forms), 1)
        self.assertEqual(forms[0]["form_selector"], "div.form-container")

    def test_detect_buttons_and_inputs(self):
        self.mock_element.exists.side_effect = lambda s: s in ("button", "input")
        
        buttons = self.pi.detect_buttons()
        self.assertIn("button", buttons)

        inputs = self.pi.detect_inputs()
        self.assertIn("input", inputs)

    def test_detect_tables(self):
        self.mock_element.exists.side_effect = lambda s: s == "table"
        tables = self.pi.detect_tables()
        self.assertEqual(len(tables), 1)
        self.assertEqual(tables[0]["selector"], "table")

    def test_recommend_next_action(self):
        self.assertEqual(
            self.pi.recommend_next_action("login"),
            "Fill login credentials and submit the form."
        )
        self.assertEqual(
            self.pi.recommend_next_action("unknown"),
            "Explore website page elements and navigate further."
        )

    def test_confidence_score(self):
        # Login confidence
        score = self.pi.confidence_score("login", ["#password"], ["button"])
        self.assertEqual(score, 1.0)  # 0.5 base + 0.3 password + 0.2 button

        # Search confidence
        score = self.pi.confidence_score("search", ["#search-box"], [])
        self.assertEqual(score, 0.9)  # 0.5 base + 0.4 search term

        # Unknown confidence
        score = self.pi.confidence_score("unknown", [], [])
        self.assertEqual(score, 0.2)

    def test_analyze_flow(self):
        self.mock_playwright.is_browser_running.return_value = False
        self.mock_analyzer.analyze_page.return_value = {
            "url": "https://test.com/login",
            "title": "Welcome login",
        }
        self.mock_element.exists.side_effect = lambda s: s in ("#password", "button")

        result = self.pi.analyze()
        self.assertIsInstance(result, PageAnalysisResult)
        self.assertEqual(result.url, "https://test.com/login")
        self.assertEqual(result.page_type, "login")
        self.assertEqual(result.confidence, 1.0)
        self.assertEqual(
            result.recommended_next_action,
            "Fill login credentials and submit the form."
        )


if __name__ == "__main__":
    unittest.main()
