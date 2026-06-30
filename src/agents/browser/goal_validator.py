"""Goal Validator for RAYZEN AI.

This module validates that a ``Goal`` contains the required fields, supported
types, and all necessary entities based on the goal type before planning begins.
"""

from typing import List, Dict, Set
from .goal_models import Goal

# Define the required entities for each supported goal type.
REQUIRED_ENTITIES: Dict[str, Set[str]] = {
    "search": {"query"},
    "login": {"login_url", "username", "password"},
}

class GoalValidator:
    """Validates ``Goal`` instances to ensure they are well‑formed.

    Checks:
    1. The goal type is non‑empty and supported.
    2. All required entities for that goal type are present.
    3. Entities have non‑empty/valid values.
    """

    def __init__(self, supported_types: Dict[str, Set[str]] | None = None):
        self.supported_types = supported_types if supported_types is not None else REQUIRED_ENTITIES

    def validate(self, goal: Goal) -> bool:
        """Validates the given ``Goal``.

        Raises:
            ValueError: If the goal type is unsupported, missing, or required entities are absent.

        Returns:
            True if the goal is valid.
        """
        if not goal.type:
            raise ValueError("Goal type must not be empty.")

        if goal.type not in self.supported_types:
            raise ValueError(f"Unsupported goal type: '{goal.type}'. Supported types: {list(self.supported_types.keys())}")

        required = self.supported_types[goal.type]
        missing = required - set(goal.entities.keys())
        if missing:
            raise ValueError(f"Missing required entities for goal type '{goal.type}': {list(missing)}")

        # Ensure required entities are not empty/None
        for key in required:
            val = goal.entities.get(key)
            if val is None or (isinstance(val, str) and not val.strip()):
                raise ValueError(f"Required entity '{key}' cannot be empty or None.")

        return True
