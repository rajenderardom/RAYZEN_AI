"""
RAYZEN AI
AI Brain Task Planner

Version : 0.1.0
"""

from typing import List
from src.brain.intent_analyzer import IntentAnalyzer


class TaskPlanner:
    """Generates sequential execution steps based on analyzed user request intents."""

    def __init__(self, intent_analyzer: IntentAnalyzer):
        """Initialize TaskPlanner.

        Args:
            intent_analyzer (IntentAnalyzer): Intent analyzer instance.
        """
        self.analyzer = intent_analyzer
        self.logger = intent_analyzer.logger

        # Capitalization map for browser targets
        self._browser_names = {
            "google": "Google",
            "github": "GitHub",
            "chatgpt": "ChatGPT",
        }

    def create_plan(self, user_request: str) -> List[str]:
        """Generate ordered execution steps for the user request.

        Args:
            user_request (str): The raw user request string.

        Returns:
            List[str]: An ordered list of plan steps, or empty list if no plan could be formed.
        """
        if not isinstance(user_request, str):
            self.logger.error("Task planning failed: Request must be a string.")
            return []

        try:
            self.logger.info(f"Generating plan for request: '{user_request}'")
            intent_data = self.analyzer.analyze(user_request)
            intent = intent_data.get("intent", "unknown")

            if intent == "desktop.open":
                target = intent_data.get("target", "")
                display_target = "File Explorer" if target == "explorer" else target.title()
                plan = [f"Launch {display_target}"]
                self.logger.info(f"Desktop open plan generated: {plan}")
                return plan

            elif intent == "browser.open":
                target = intent_data.get("target", "")
                display_target = self._browser_names.get(target.lower(), target.title())
                plan = ["Launch Browser", f"Open {display_target}"]
                self.logger.info(f"Browser open plan generated: {plan}")
                return plan

            elif intent == "excel.analyze":
                filename = intent_data.get("file", "")
                plan = [
                    f"Load Workbook: {filename}",
                    "Analyze Sheet Structure",
                    "Calculate Sheet Dimensions",
                ]
                self.logger.info(f"Excel analysis plan generated: {plan}")
                return plan

            elif intent == "browser.workflow":
                # Matches the standard workflow planning steps requested in the prompt
                plan = [
                    "Launch Browser",
                    "Open Website",
                    "Login",
                    "Navigate",
                    "Download File",
                    "Verify Download",
                ]
                self.logger.info(f"Browser workflow plan generated: {plan}")
                return plan

            else:
                self.logger.info(f"No execution plan could be generated for intent: '{intent}'")
                return []

        except Exception as e:
            self.logger.error(f"Error occurred during task planning: {e}")
            return []
