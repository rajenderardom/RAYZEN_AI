"""
RAYZEN AI
Browser Action Planner

Version : 0.1.0
"""

import re
from typing import List, Dict, Any
from src.core.logger import RayzenLogger


class ActionPlanner:
    """Generates structured browser workflow action steps based on user instructions and active page state analysis."""

    def __init__(self):
        self.logger = RayzenLogger()

    def plan_actions(self, instruction: str, page_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate structured execution steps based on instruction and scanned page structure.

        Args:
            instruction (str): User natural language instruction.
            page_analysis (Dict[str, Any]): Analyzed page layout details.

        Returns:
            List[Dict[str, Any]]: List of step dictionaries.
        """
        self.logger.info(f"Planning browser actions for instruction: '{instruction}'")
        steps: List[Dict[str, Any]] = []
        inst_lower = instruction.lower().strip()

        # 1. Check for explicit URL navigation request
        url_match = re.search(r"(?:open|navigate|go to)\s+(https?://[^\s]+)", instruction, re.IGNORECASE)
        if url_match:
            steps.append({"action": "open_url", "url": url_match.group(1)})
            return steps

        # 2. Check for portal login intent
        if "login" in inst_lower or "sign in" in inst_lower:
            # Plan login flow if input selectors were detected
            inputs = page_analysis.get("inputs", [])
            buttons = page_analysis.get("buttons", [])

            username_sel = next((s for s in inputs if "user" in s or "email" in s), None) or (inputs[0] if inputs else "#username")
            password_sel = next((s for s in inputs if "pass" in s), None) or (inputs[1] if len(inputs) > 1 else "#password")
            submit_sel = next((b for b in buttons if "submit" in b or "login" in b or "btn" in b), None) or (buttons[0] if buttons else "#submit-btn")

            steps.extend([
                {"action": "wait_for_selector", "selector": username_sel},
                {"action": "type", "selector": username_sel, "text": "admin"},
                {"action": "type", "selector": password_sel, "text": "password123"},
                {"action": "click", "selector": submit_sel},
                {"action": "wait", "duration": 2000}
            ])
            return steps

        # 3. Check for search request
        if "search" in inst_lower or "find" in inst_lower:
            query = "RAYZEN AI"
            words = instruction.split()
            if len(words) > 1:
                # Extract text after 'search' or 'find'
                for idx, w in enumerate(words):
                    if w.lower() in ("search", "find") and idx < len(words) - 1:
                        query = " ".join(words[idx + 1:])
                        break

            inputs = page_analysis.get("inputs", [])
            search_sel = next((s for s in inputs if "search" in s or "q" in s or "input" in s), None) or (inputs[0] if inputs else "input[name='q']")

            steps.extend([
                {"action": "type", "selector": search_sel, "text": query},
                {"action": "press", "key": "Enter"},
                {"action": "wait", "duration": 2000}
            ])
            return steps

        # Default fallback sequence: navigate to Google and search instruction text
        steps.append({"action": "open_url", "url": "https://www.google.com"})
        return steps
