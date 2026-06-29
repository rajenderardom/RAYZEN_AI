"""
RAYZEN AI
AI Skill Selector

Version : 0.1.0
"""

from typing import Dict, Any
from src.core.skill_registry import SkillRegistry
from src.core.logger import RayzenLogger


class SkillSelector:
    """Selects the best matching registered skill for a parsed user request intent."""

    def __init__(self, skill_registry: SkillRegistry):
        """Initialize SkillSelector.

        Args:
            skill_registry (SkillRegistry): Central registry of available skills.
        """
        self.registry = skill_registry
        self.logger = RayzenLogger()

        # Dynamic intent prefix to skill name map
        self._intent_mappings: Dict[str, str] = {
            "browser": "browser",
            "desktop": "desktop",
            "excel": "excel",
        }

    def register_mapping(self, intent_prefix: str, skill_name: str) -> None:
        """Register a custom intent prefix to skill mapping dynamically.

        Args:
            intent_prefix (str): Prefix of the intent (e.g. 'pdf').
            skill_name (str): Skill identifier in the registry.
        """
        if not isinstance(intent_prefix, str) or not isinstance(skill_name, str):
            self.logger.error("Mapping registration failed: Types must be string.")
            return

        prefix = intent_prefix.strip().lower()
        name = skill_name.strip().lower()
        self._intent_mappings[prefix] = name
        self.logger.info(f"Registered intent mapping: '{prefix}' -> skill '{name}'")

    def select_skill(self, intent: str, intent_confidence: float = 1.0) -> Dict[str, Any]:
        """Match intent to registered skills and return the best matching skill details.

        Args:
            intent (str): Dotted intent string (e.g. 'browser.open', 'excel.analyze').
            intent_confidence (float): Confidence score of the intent. Defaults to 1.0.

        Returns:
            Dict[str, Any]: Selected skill details.
        """
        self.logger.info(
            f"Selecting skill for intent: '{intent}' (intent confidence={intent_confidence})"
        )

        if not isinstance(intent, str) or not intent.strip():
            self.logger.error("Skill selection failed: Intent must be a non-empty string.")
            return {"skill": "unknown", "confidence": 0.0}

        try:
            # 1. Retrieve available skills from the registry
            available_skills = self.registry.list_skills()
            available_set = {s.lower() for s in available_skills}

            # 2. Extract intent prefix (e.g. 'browser' from 'browser.open')
            intent_lower = intent.strip().lower()
            parts = intent_lower.split(".")
            prefix = parts[0] if parts else intent_lower

            # 3. Check registered mapping first
            target_skill = self._intent_mappings.get(prefix)

            # If mapping is not set but prefix itself is in available registry, default to prefix
            if not target_skill and prefix in available_set:
                target_skill = prefix

            # 4. Validate if matched target exists in registry
            if target_skill and target_skill in available_set:
                self.logger.info(f"Skill '{target_skill}' selected successfully for intent '{intent}'.")
                return {"skill": target_skill, "confidence": round(intent_confidence, 2)}

            # 5. Check fallback substring matches for robustness
            for skill in available_skills:
                skill_lower = skill.lower()
                if skill_lower in intent_lower or intent_lower in skill_lower:
                    self.logger.info(
                        f"Skill '{skill}' matched via substring fallback for intent '{intent}'."
                    )
                    return {
                        "skill": skill_lower,
                        "confidence": round(intent_confidence * 0.9, 2),  # Reduce confidence slightly for fallback
                    }
                # Check parts split by underscore for prefix/suffix match
                parts = skill_lower.split("_")
                for part in parts:
                    if len(part) > 2 and (part in intent_lower or intent_lower in part):
                        self.logger.info(
                            f"Skill '{skill}' matched via part '{part}' fallback for intent '{intent}'."
                        )
                        return {
                            "skill": skill_lower,
                            "confidence": round(intent_confidence * 0.9, 2),
                        }



            self.logger.warning(f"No matching skill found for intent: '{intent}'.")
            return {"skill": "unknown", "confidence": 0.0}

        except Exception as e:
            self.logger.error(f"Error occurred during skill selection: {e}")
            return {"skill": "unknown", "confidence": 0.0}
