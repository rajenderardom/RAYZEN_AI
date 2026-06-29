"""
RAYZEN AI
Office Agent Context

Version : 0.1.0
"""

from typing import Dict, Any
import threading


class OfficeContext:
    """Manages thread-safe session properties and workspace variables for the Office Agent."""

    def __init__(self):
        self._lock = threading.Lock()
        self._variables: Dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        with self._lock:
            self._variables[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        with self._lock:
            return self._variables.get(key, default)

    def clear(self) -> None:
        with self._lock:
            self._variables.clear()

    def get_all(self) -> Dict[str, Any]:
        with self._lock:
            return self._variables.copy()
