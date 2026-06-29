"""
RAYZEN AI
Browser Agent Orchestrator

Version : 0.1.0
"""

import datetime
import uuid
from typing import Dict, Any, Optional
from src.core.logger import RayzenLogger
from src.core.skill_registry import SkillRegistry
from src.agents.browser.browser_models import BrowserTaskRecord, BrowserAgentState
from src.agents.browser.browser_context import BrowserContext
from src.agents.browser.page_analyzer import PageAnalyzer
from src.agents.browser.action_planner import ActionPlanner
from src.agents.browser.execution_monitor import ExecutionMonitor
from src.agents.browser.recovery_engine import RecoveryEngine


class BrowserAgent:
    """Intelligent browser agent coordinating page analysis, action planning, and execution monitors."""

    def __init__(self, skill_registry: SkillRegistry):
        """Initialize BrowserAgent.

        Args:
            skill_registry (SkillRegistry): Skill registry containing browser systems.
        """
        self.registry = skill_registry
        self.logger = RayzenLogger()
        self.context = BrowserContext()
        self.state = BrowserAgentState()

        # Browser Agent internal modules
        self.analyzer = PageAnalyzer()
        self.planner = ActionPlanner()
        self.monitor = ExecutionMonitor()
        self.recovery = RecoveryEngine()

        # Task history audit records
        self._history: list[BrowserTaskRecord] = []

    def get_history(self) -> list[BrowserTaskRecord]:
        """Retrieve task history records."""
        return list(self._history)

    def execute(self, task: str) -> bool:
        """Analyze, plan, and execute a browser automation instruction thread-safely.

        Args:
            task (str): The natural language instruction.

        Returns:
            bool: True on success, False on failure.
        """
        task_id = str(uuid.uuid4())[:8]
        self.logger.info(f"BrowserAgent: Starting task [{task_id}]: '{task}'")

        record = BrowserTaskRecord(task_id=task_id, description=task)
        self._history.append(record)

        # Retrieve browser infrastructure from SkillRegistry
        playwright = self.registry.get("playwright_engine")
        page_control = self.registry.get("page_controller")
        element_engine = self.registry.get("element_engine")
        runner = self.registry.get("workflow_runner")

        if not all([playwright, page_control, element_engine, runner]):
            self.logger.error("BrowserAgent failed: Required browser skills are not registered.")
            record.status = "failed"
            record.completed_at = datetime.datetime.now()
            record.error_message = "Missing core browser skills in registry."
            return False

        try:
            # 1. Ensure browser is launched
            if not playwright.is_browser_running():
                self.logger.info("BrowserAgent: Browser not running, launching browser instance...")
                if not playwright.launch_browser(headless=False):
                    raise RuntimeError("Failed to launch playwright browser.")

            # 2. Analyze current page DOM structure
            page_analysis = self.analyzer.analyze_page(page_control, element_engine)
            self.state.active_url = page_analysis.get("url")
            self.state.page_title = page_analysis.get("title")

            # 3. Plan automation steps
            steps = self.planner.plan_actions(task, page_analysis)
            record.steps = [step.get("action", "unknown") for step in steps]

            # 4. Monitor execution steps
            success = self.monitor.execute_and_monitor(runner, steps)
            
            # 5. Apply recovery strategies if failed
            if not success:
                self.logger.warn("BrowserAgent: Step failed, triggering page reload recovery...")
                if self.recovery.reload_page(page_control):
                    self.logger.info("BrowserAgent: Page reloaded successfully. Retrying monitor steps...")
                    success = self.monitor.execute_and_monitor(runner, steps)

            record.status = "success" if success else "failed"
            record.completed_at = datetime.datetime.now()
            
            if not success:
                record.error_message = "Execution monitor reported step failures."

            self.logger.info(f"BrowserAgent: Task [{task_id}] execution finished. Status: {record.status}")
            return success

        except Exception as e:
            record.status = "failed"
            record.completed_at = datetime.datetime.now()
            record.error_message = str(e)
            self.logger.error(f"BrowserAgent: Task [{task_id}] failed with exception: {e}")
            return False
