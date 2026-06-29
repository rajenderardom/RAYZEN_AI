"""
RAYZEN AI
Skill Registry

Version : 0.1.0
"""

import threading
from typing import Dict, Any, List
from src.core.logger import RayzenLogger


class SkillRegistry:
    """Central registry and dispatcher for execution skills (Browser, Desktop, Excel, etc.)."""

    def __init__(self):
        """Initialize SkillRegistry with thread synchronization locks."""
        self.logger = RayzenLogger()
        self._skills: Dict[str, Any] = {}
        self._lock = threading.Lock()

    def register(self, skill_name: str, skill_instance: Any) -> None:
        """Register a new skill instance thread-safely.

        Args:
            skill_name (str): Name identifier for the skill (e.g. 'desktop', 'browser').
            skill_instance (Any): The instantiated skill class/object.
        """
        if not isinstance(skill_name, str):
            self.logger.error("Skill registration failed: Name must be a string.")
            return

        with self._lock:
            self._skills[skill_name.strip().lower()] = skill_instance
            self.logger.info(f"Skill registered successfully: '{skill_name}'")

    def unregister(self, skill_name: str) -> None:
        """Unregister an existing skill instance thread-safely.

        Args:
            skill_name (str): Name identifier of the skill to remove.
        """
        if not isinstance(skill_name, str):
            return

        key = skill_name.strip().lower()
        with self._lock:
            if key in self._skills:
                del self._skills[key]
                self.logger.info(f"Skill unregistered successfully: '{skill_name}'")
            else:
                self.logger.warning(f"Failed to unregister: Skill '{skill_name}' not found.")

    def get(self, skill_name: str) -> Any:
        """Retrieve a registered skill instance.

        Args:
            skill_name (str): Name identifier of the skill.

        Returns:
            Any: The registered skill instance, or None if not found.
        """
        if not isinstance(skill_name, str):
            return None

        key = skill_name.strip().lower()
        with self._lock:
            skill = self._skills.get(key)
            if not skill:
                self.logger.warning(f"Skill lookup failed: '{skill_name}' not found.")
            return skill

    def list_skills(self) -> List[str]:
        """List all registered skill names in sorted order.

        Returns:
            List[str]: List of skill names.
        """
        with self._lock:
            skills_list = sorted(self._skills.keys())
            self.logger.info(f"Listing registered skills: {skills_list}")
            return skills_list

    def execute(self, skill_name: str, action: str, **kwargs) -> Any:
        """Dynamically execute a method action on a registered skill instance.

        Args:
            skill_name (str): Name identifier of the target skill.
            action (str): Method name to invoke on the skill instance.
            **kwargs: Keyword arguments passed to the method.

        Returns:
            Any: The return value of the skill action, or False on failure.
        """
        self.logger.info(
            f"Requesting skill execution: '{skill_name}.{action}' with params: {kwargs}"
        )

        skill_instance = self.get(skill_name)
        if not skill_instance:
            self.logger.error(f"Skill execution failed: Unknown skill: '{skill_name}'")
            return False

        try:
            method = getattr(skill_instance, action, None)
            if not method or not callable(method):
                self.logger.error(
                    f"Skill execution failed: Action '{action}' is not callable on skill '{skill_name}'"
                )
                return False

            self.logger.info(f"Executing action '{action}' on skill '{skill_name}'")
            result = method(**kwargs)
            self.logger.info(f"Execution completed: '{skill_name}.{action}' returned: {result}")
            return result

        except Exception as e:
            self.logger.error(f"Exception occurred executing '{skill_name}.{action}': {e}")
            return False
