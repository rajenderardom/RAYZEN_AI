"""
RAYZEN AI
Workflow Loader

Version : 0.1.0
"""

import os
import json
from typing import Dict, Any
from src.core.logger import RayzenLogger


class WorkflowLoader:
    """Manages reading, writing, and validating browser automation workflows stored as JSON files."""

    def __init__(self):
        """Initialize WorkflowLoader."""
        self.logger = RayzenLogger()

    def validate(self, workflow: Dict[str, Any]) -> bool:
        """Validate if the workflow dictionary matches the structural layout rules.

        Args:
            workflow (Dict[str, Any]): Workflow definition to check.

        Returns:
            bool: True if valid, False otherwise.
        """
        if not isinstance(workflow, dict):
            self.logger.error("Workflow validation failed: Workflow must be a dictionary.")
            return False

        # Verify required root level attributes
        for key in ["name", "version", "steps"]:
            if key not in workflow:
                self.logger.error(f"Workflow validation failed: Missing required key '{key}'.")
                return False

        if not isinstance(workflow["name"], str) or not workflow["name"].strip():
            self.logger.error(
                "Workflow validation failed: Root key 'name' must be a non-empty string."
            )
            return False

        if not isinstance(workflow["version"], str) or not workflow["version"].strip():
            self.logger.error(
                "Workflow validation failed: Root key 'version' must be a non-empty string."
            )
            return False

        steps = workflow["steps"]
        if not isinstance(steps, list):
            self.logger.error("Workflow validation failed: Root key 'steps' must be a list.")
            return False

        # Every step must contain a valid action key
        for idx, step in enumerate(steps, 1):
            if not isinstance(step, dict):
                self.logger.error(f"Workflow validation failed: Step {idx} must be a dictionary.")
                return False
            if "action" not in step:
                self.logger.error(
                    f"Workflow validation failed: Step {idx} is missing required key 'action'."
                )
                return False
            if not isinstance(step["action"], str) or not step["action"].strip():
                self.logger.error(
                    f"Workflow validation failed: Step {idx} 'action' must be a non-empty string."
                )
                return False

        return True

    def load(self, file_path: str) -> Dict[str, Any]:
        """Load and validate a workflow JSON definition file.

        Args:
            file_path (str): Path to the workflow file.

        Returns:
            Dict[str, Any]: Parsed and validated workflow details, or empty dict on failure.
        """
        self.logger.info(f"Loading workflow file from: '{file_path}'")
        if not os.path.exists(file_path):
            self.logger.error(f"Workflow load failed: File does not exist: {file_path}")
            return {}

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not self.validate(data):
                self.logger.error(
                    f"Workflow load failed: Validation failed for file '{file_path}'."
                )
                return {}

            self.logger.info(
                f"Workflow loaded successfully: '{data.get('name')}' (v{data.get('version')})"
            )
            return data
        except Exception as e:
            self.logger.error(f"Exception occurred while loading workflow from '{file_path}': {e}")
            return {}

    def save(self, file_path: str, workflow: Dict[str, Any]) -> bool:
        """Serialize and save a validated workflow dictionary to disk as JSON.

        Args:
            file_path (str): Destination output file path.
            workflow (Dict[str, Any]): Workflow dictionary contents to write.

        Returns:
            bool: True on success, False on failure.
        """
        self.logger.info(f"Saving workflow to file: '{file_path}'")
        if not self.validate(workflow):
            self.logger.error("Workflow save failed: Validation of target workflow dict failed.")
            return False

        try:
            # Ensure target directory exists
            dir_name = os.path.dirname(os.path.abspath(file_path))
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(workflow, f, indent=4)

            self.logger.info(f"Workflow saved successfully to: '{file_path}'")
            return True
        except Exception as e:
            self.logger.error(f"Exception occurred while saving workflow to '{file_path}': {e}")
            return False
