"""
RAYZEN AI
Natural Language Interpreter

Version : 0.1.0
"""

from typing import Dict


class NaturalLanguageInterpreter:
    """Interprets natural language inputs into standardized command strings."""

    def __init__(self):
        """Initialize the interpreter with standard phrasing mappings."""
        self._mappings: Dict[str, str] = {
            "google kholo": "open google",
            "calculator kholo": "open calculator",
            "chatgpt kholo": "open chatgpt",
            "paint kholo": "open paint",
            "notepad kholo": "open notepad",
            "explorer kholo": "open explorer",
            "github kholo": "open github",
            "open my browser": "open google",
        }

    def interpret(self, text: str) -> str:
        """Interpret natural language text into standard command engine command.

        Args:
            text (str): Natural language input query.

        Returns:
            str: Normalized matching command if found; original query text otherwise.
        """
        if not isinstance(text, str):
            return text

        normalized = text.strip().lower()
        if normalized in self._mappings:
            return self._mappings[normalized]

        return text
