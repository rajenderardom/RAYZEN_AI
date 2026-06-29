"""
RAYZEN AI
Browser Execution Monitor

Version : 0.1.0
"""

from typing import List, Dict, Any
from src.core.logger import RayzenLogger


class ExecutionMonitor:
    """Monitors step execution, logging progress and capturing screenshots on failure."""

    def __init__(self):
        self.logger = RayzenLogger()

    def execute_and_monitor(self, runner, steps: List[Dict[str, Any]]) -> bool:
        """Executes workflow steps sequentially and monitors execution success.

        Args:
            runner: WorkflowRunner instance.
            steps (List[Dict[str, Any]]): Planned step dictionaries.

        Returns:
            bool: True if all steps completed successfully, False otherwise.
        """
        self.logger.info(f"Starting execution monitor for {len(steps)} steps...")
        
        for idx, step in enumerate(steps, 1):
            action = step.get("action")
            self.logger.info(f"Monitor: Running step {idx}/{len(steps)}: '{action}'")

            # Validate step signature
            if not runner.validate(step):
                self.logger.error(f"Monitor: Step validation failed at index {idx} for action '{action}'")
                self._capture_failure_fallback(runner)
                return False

            # Run step
            try:
                success = runner.execute_step(step)
                if not success:
                    self.logger.error(f"Monitor: Step execution failed at index {idx} for action '{action}'")
                    self._capture_failure_fallback(runner)
                    return False
            except Exception as e:
                self.logger.exception(f"Monitor: Exception raised executing step {idx} ({action}): {e}")
                self._capture_failure_fallback(runner)
                return False

        self.logger.info("Monitor: All planned steps executed successfully.")
        return True

    def _capture_failure_fallback(self, runner) -> None:
        """Capture screenshot to data directory on step failures if browser is running."""
        try:
            if runner.playwright.is_browser_running() and runner.playwright._page:
                import os
                screenshot_path = "data/error_snapshots/failure_screenshot.png"
                os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
                self.logger.warn(f"Monitor: Attempting recovery screenshot to: '{screenshot_path}'")
                runner.playwright._page.screenshot(path=screenshot_path)
        except Exception as e:
            self.logger.error(f"Monitor: Failed to capture failure screenshot: {e}")
