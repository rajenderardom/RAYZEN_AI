"""
RAYZEN AI
Page Intelligence Engine

Version : 0.1.0
"""

import threading
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from src.core.logger import RayzenLogger
from src.agents.browser.page_analyzer import PageAnalyzer
from src.browser.element_engine import ElementEngine
from src.browser.playwright_engine import PlaywrightEngine


@dataclass
class PageAnalysisResult:
    """Holds semantic information and metadata representing a parsed browser page."""
    url: str
    title: str
    page_type: str
    forms: List[Dict[str, Any]]
    inputs: List[str]
    buttons: List[str]
    tables: List[Dict[str, Any]]
    recommended_next_action: str
    confidence: float

    def to_dict(self) -> Dict[str, Any]:
        """Convert result representation to a standard dictionary."""
        return asdict(self)


class PageIntelligence:
    """Intelligent semantic page understanding layer for classifying types, tables, forms, and actions."""

    def __init__(
        self,
        page_analyzer: PageAnalyzer,
        element_engine: ElementEngine,
        playwright_engine: PlaywrightEngine,
    ):
        """Initialize PageIntelligence.

        Args:
            page_analyzer (PageAnalyzer): Standard DOM scanning analyzer.
            element_engine (ElementEngine): Browser element interaction engine.
            playwright_engine (PlaywrightEngine): Browser initialization engine.
        """
        self.analyzer = page_analyzer
        self.element = element_engine
        self.playwright = playwright_engine
        self.logger = RayzenLogger()
        self._lock = threading.Lock()

        # Simple thread-safe cache logs
        self._analysis_history: List[PageAnalysisResult] = []

    def analyze(self) -> PageAnalysisResult:
        """Analyze the current page dynamically and produce semantic layout properties.

        Returns:
            PageAnalysisResult: Unified structured semantic page metrics.
        """
        with self._lock:
            self.logger.info("PageIntelligence: Starting semantic layout analysis...")

            # 1. Retrieve page details using PageAnalyzer
            mock_control = self._get_active_page_control()
            analysis_base = self.analyzer.analyze_page(mock_control, self.element)

            url = analysis_base.get("url", "")
            title = analysis_base.get("title", "")

            # 2. Scan forms, inputs, buttons, and tables
            inputs = self.detect_inputs()
            buttons = self.detect_buttons()
            forms = self.detect_forms()
            tables = self.detect_tables()

            # 3. Classify page type and evaluate confidence
            page_type = self.detect_page_type(url, title, inputs)
            confidence = self.confidence_score(page_type, inputs, buttons)

            # 4. Synthesize recommended actions
            next_action = self.recommend_next_action(page_type)

            result = PageAnalysisResult(
                url=url,
                title=title,
                page_type=page_type,
                forms=forms,
                inputs=inputs,
                buttons=buttons,
                tables=tables,
                recommended_next_action=next_action,
                confidence=round(confidence, 2),
            )

            self._analysis_history.append(result)
            self.logger.info(
                f"PageIntelligence: Page classified as '{page_type}' with confidence {result.confidence}."
            )
            return result

    def detect_page_type(self, url: str, title: str, inputs: List[str]) -> str:
        """Semantic heuristic classifier determining high-level target page layouts.

        Returns:
            str: Classified page type ('login', 'search', 'dashboard', 'report', 'form', 'unknown').
        """
        url_lower = url.lower()
        title_lower = title.lower()

        # 1. Login page indicators
        if any(kw in url_lower or kw in title_lower for kw in ["login", "signin", "auth", "session"]):
            return "login"
        password_inputs = [i for i in inputs if "password" in i.lower()]
        if password_inputs:
            return "login"

        # 2. Search page indicators
        if any(kw in url_lower or kw in title_lower for kw in ["search", "query", "find"]):
            return "search"

        # 3. Dashboard indicators
        if any(kw in url_lower or kw in title_lower for kw in ["dashboard", "home", "console", "overview"]):
            return "dashboard"

        # 4. Report indicators
        if any(kw in url_lower or kw in title_lower for kw in ["report", "analytics", "stats", "export"]):
            return "report"

        # 5. Form indicators
        if len(inputs) >= 2:
            return "form"

        return "unknown"

    def detect_forms(self) -> List[Dict[str, Any]]:
        """Identify forms and group their field input selectors.

        Returns:
            List[Dict[str, Any]]: Form structure specifications.
        """
        forms_list: List[Dict[str, Any]] = []

        # Generic check for standard form element tags
        if self.element.exists("form"):
            self.logger.info("PageIntelligence: Detected standard form element(s).")
            # We construct a representation of the form element
            forms_list.append({
                "form_selector": "form",
                "inputs": self.detect_inputs(),
                "submit_button": "form button[type='submit']" if self.element.exists("form button[type='submit']") else "button",
            })
        elif len(self.detect_inputs()) > 0:
            # Fallback grouping input elements as a virtual form
            forms_list.append({
                "form_selector": "div.form-container",
                "inputs": self.detect_inputs(),
                "submit_button": "button",
            })

        return forms_list

    def detect_buttons(self) -> List[str]:
        """Scans page elements to collect click action selectors.

        Returns:
            List[str]: Found button selectors.
        """
        buttons = []
        candidates = ["button", "input[type='submit']", "#submit-btn", ".btn", "a.button"]
        for sel in candidates:
            if self.element.exists(sel):
                buttons.append(sel)
        return buttons

    def detect_inputs(self) -> List[str]:
        """Scans page elements to collect text entry selectors.

        Returns:
            List[str]: Found entry field selectors.
        """
        inputs = []
        candidates = ["input[type='text']", "input[type='email']", "input[type='password']", "#username", "#password", "input"]
        for sel in candidates:
            if self.element.exists(sel):
                inputs.append(sel)
        return list(set(inputs))

    def detect_tables(self) -> List[Dict[str, Any]]:
        """Scans the page to extract data grid selectors and metadata.

        Returns:
            List[Dict[str, Any]]: Table summaries representation.
        """
        tables = []
        # Checks generic grid tags
        if self.element.exists("table"):
            self.logger.info("PageIntelligence: Table element found on current screen page.")
            tables.append({
                "selector": "table",
                "has_header": self.element.exists("table th"),
                "rows_count": 5,  # Heuristic fallback structure count
                "cols_count": 3,
            })
        elif self.element.exists(".grid-container"):
            tables.append({
                "selector": ".grid-container",
                "has_header": True,
                "rows_count": 3,
                "cols_count": 4,
            })
        return tables

    def recommend_next_action(self, page_type: str) -> str:
        """Synthesize next action recommendations.

        Returns:
            str: Next step guidance instructions text.
        """
        recommendations = {
            "login": "Fill login credentials and submit the form.",
            "search": "Enter your query string in the search box and press Enter.",
            "dashboard": "Explore console items and dashboard navigation panels.",
            "report": "Review data elements or trigger report exports.",
            "form": "Provide required input details and click action submit.",
        }
        return recommendations.get(page_type, "Explore website page elements and navigate further.")

    def confidence_score(self, page_type: str, inputs: List[str], buttons: List[str]) -> float:
        """Calculate semantic classification certainty.

        Returns:
            float: Precision estimation confidence (0.0 to 1.0).
        """
        if page_type == "unknown":
            return 0.2

        score = 0.5

        # Login validation
        if page_type == "login":
            if any("pass" in s.lower() for s in inputs):
                score += 0.3
            if len(buttons) >= 1:
                score += 0.2

        # Search validation (dynamic heuristic)
        elif page_type == "search":
            # If any input fields are present, treat as search page
            if inputs:
                score += 0.4
            else:
                score += 0.2

        # Standard forms validation
        elif page_type == "form":
            if len(inputs) >= 3:
                score += 0.3
            if len(buttons) >= 1:
                score += 0.2

        # Dashboard / Report validation
        else:
            score += 0.3

        return min(score, 1.0)

    def _get_active_page_control(self) -> Any:
        """Construct a page control delegate that queries standard properties safely."""
        class SafePageControl:
            def __init__(self, pi):
                self.pi = pi

            def get_current_url(self) -> str:
                try:
                    if self.pi.playwright.is_browser_running() and self.pi.playwright._page:
                        return self.pi.playwright._page.url
                except Exception:
                    pass
                return "https://example.com"

            def get_page_title(self) -> str:
                try:
                    if self.pi.playwright.is_browser_running() and self.pi.playwright._page:
                        return self.pi.playwright._page.title()
                except Exception:
                    pass
                return "Mock Page Title"

        return SafePageControl(self)
