"""
RAYZEN AI
AI Brain Intent Analyzer

Version : 0.1.0
"""

import re
from typing import Dict, Any
from src.core.interpreter import NaturalLanguageInterpreter
from src.core.logger import RayzenLogger


class IntentAnalyzer:
    """Analyzes user request queries into structured intent dictionaries using pattern matching."""

    def __init__(self, interpreter: NaturalLanguageInterpreter):
        """Initialize IntentAnalyzer.

        Args:
            interpreter (NaturalLanguageInterpreter): Natural language interpreter instance.
        """
        self.interpreter = interpreter
        self.logger = RayzenLogger()

        self._browser_targets = {"google", "github", "chatgpt"}
        self._desktop_targets = {"notepad", "calculator", "explorer", "paint"}

        self._excel_regex = re.compile(r"^analyze\s+(.+\.(?:xlsx|xls|csv))$", re.IGNORECASE)
        self._download_regex = re.compile(r"^download\s+(?:latest\s+)?(.+)$", re.IGNORECASE)

    def analyze(self, text: str) -> Dict[str, Any]:
        """Convert natural language request queries into structured intents.

        Args:
            text (str): Raw user query string.

        Returns:
            Dict[str, Any]: Structured intent details.
        """
        if not isinstance(text, str):
            self.logger.error("Intent analysis failed: Input must be a string.")
            return {"intent": "unknown", "confidence": 0.0}

        cleaned = text.strip()
        normalized = cleaned.lower()

        try:
            excel_match = self._excel_regex.match(normalized)
            if excel_match:
                raw_match = self._excel_regex.match(cleaned)
                filename = raw_match.group(1) if raw_match else excel_match.group(1)
                self.logger.info(f"Excel analysis intent identified: '{filename}'")
                return {"intent": "excel.analyze", "file": filename, "confidence": 0.95}

            download_match = self._download_regex.match(normalized)
            if download_match:
                raw_match = self._download_regex.match(cleaned)
                task_detail = raw_match.group(1) if raw_match else download_match.group(1)
                task_name = f"download {task_detail.lower()}"
                self.logger.info(f"Browser workflow intent identified: '{task_name}'")
                return {"intent": "browser.workflow", "task": task_name, "confidence": 0.80}

            standardized = self.interpreter.interpret(text)
            standardized_lower = standardized.strip().lower()

            if standardized_lower.startswith("open "):
                target = standardized_lower[5:].strip()
                if target in self._browser_targets:
                    self.logger.info(f"Browser open intent identified for target: '{target}'")
                    return {"intent": "browser.open", "target": target, "confidence": 1.0}
                elif target in self._desktop_targets:
                    self.logger.info(f"Desktop open intent identified for target: '{target}'")
                    return {"intent": "desktop.open", "target": target, "confidence": 1.0}

            self.logger.info(f"Unknown query intent fallback: '{text}'")
            return {"intent": "unknown", "confidence": 0.0}

        except Exception as e:
            self.logger.error(f"Error occurred during intent analysis: {e}")
            return {"intent": "unknown", "confidence": 0.0}
