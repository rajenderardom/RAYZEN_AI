"""
RAYZEN AI
Browser Agent Context

Version : 0.1.0
"""

import threading
from typing import Dict, Any


class BrowserContext:
    """Manages thread-safe session variables and context states for the Browser Agent."""

    def __init__(self):
        self._lock = threading.Lock()
        self._variables: Dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        """Set a context variable thread-safely."""
        with self._lock:
            self._variables[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get a context variable thread-safely."""
        with self._lock:
            return self._variables.get(key, default)

    def clear(self) -> None:
        """Clear all context variables thread-safely."""
        with self._lock:
            self._variables.clear()

    def get_all(self) -> Dict[str, Any]:
        """Get a copy of all context variables thread-safely."""
        with self._lock:
            return self._variables.copy()
