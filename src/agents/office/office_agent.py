"""
RAYZEN AI
Office Agent Orchestrator

Version : 0.1.0
"""

import os
import zipfile
import datetime
import uuid
from typing import Dict, Any, Optional
from src.core.logger import RayzenLogger
from src.core.skill_registry import SkillRegistry
from src.agents.office.office_context import OfficeContext
from src.agents.office.office_history import OfficeHistory
from src.agents.office.office_task_router import OfficeTaskRouter
from src.agents.office.office_models import TaskRecord


class OfficeAgent:
    """Main orchestrator agent managing execution contexts, task histories, routing, and skill calls."""

    def __init__(self, skill_registry: SkillRegistry):
        """Initialize OfficeAgent.

        Args:
            skill_registry (SkillRegistry): Injected skills container.
        """
        self.registry = skill_registry
        self.logger = RayzenLogger()
        self.context = OfficeContext()
        self.history = OfficeHistory()
        self.router = OfficeTaskRouter()

    def execute(self, task: str) -> bool:
        """Route and execute a natural language task description.

        Args:
            task (str): Task description prompt.

        Returns:
            bool: True on success, False on failure.
        """
        task_id = str(uuid.uuid4())[:8]
        self.logger.info(f"Agent starting task [{task_id}]: '{task}'")

        record = TaskRecord(task_id=task_id, description=task)
        self.history.add_record(record)

        method_name, args = self.router.route(task)
        if not method_name:
            self.logger.error(f"Task [{task_id}] failed: No matching method routed.")
            record.status = "failed"
            record.completed_at = datetime.datetime.now()
            record.error_message = "No task routing match found."
            return False

        try:
            self.logger.info(f"Task [{task_id}] routed to method '{method_name}' with args {args}")
            method = getattr(self, method_name)
            success = method(**args)

            record.status = "success" if success else "failed"
            record.completed_at = datetime.datetime.now()
            record.metadata = {"args": args, "method": method_name}

            if not success:
                record.error_message = f"Execution returned False inside method '{method_name}'"

            self.logger.info(f"Task [{task_id}] finished execution. Status: {record.status}")
            return success

        except Exception as e:
            record.status = "failed"
            record.completed_at = datetime.datetime.now()
            record.error_message = str(e)
            self.logger.error(f"Task [{task_id}] failed with exception: {e}")
            return False

    def compare_excel(
        self,
        old_file: str,
        new_file: str,
        key_column: str,
        sheet_name: str,
        export_path: str,
    ) -> bool:
        """Compare two spreadsheets using ExcelComparator skill.

        Returns:
            bool: True on success, False on failure.
        """
        self.logger.info(f"compare_excel running on: '{old_file}' and '{new_file}'")

        comparator = self.registry.get("excel_comparator")
        if not comparator:
            self.logger.error("compare_excel failed: 'excel_comparator' skill is not registered.")
            return False

        try:
            return self.registry.execute(
                "excel_comparator",
                "compare",
                file_path_old=old_file,
                file_path_new=new_file,
                key_column=key_column,
                sheet_name=sheet_name,
                export_path=export_path,
            )
        except Exception as e:
            self.logger.error(f"Exception raised in compare_excel skill execute: {e}")
            return False

    def generate_report(self) -> bool:
        """Runs the dashboard spreadsheet generation workflow from JSON libraries."""
        self.logger.info("generate_report running via browser workflows.")
        return self.run_workflow("workflows/office/generate_report.json")

    def run_workflow(self, file_path: str) -> bool:
        """Load and execute JSON workflow files.

        Args:
            file_path (str): Path to JSON workflow definition.

        Returns:
            bool: True on success, False on failure.
        """
        self.logger.info(f"run_workflow loading file: '{file_path}'")

        loader = self.registry.get("workflow_loader")
        runner = self.registry.get("workflow_runner")

        if not loader or not runner:
            self.logger.error("run_workflow failed: loader or runner skills not registered.")
            return False

        try:
            workflow_data = loader.load(file_path)
            if not workflow_data:
                self.logger.error(f"run_workflow failed: Could not load workflow from '{file_path}'")
                return False

            steps = workflow_data.get("steps", [])
            return runner.run(steps)
        except Exception as e:
            self.logger.error(f"Exception raised in run_workflow: {e}")
            return False

    def draft_email(self, recipient: str, subject: str, body: str, export_path: str) -> bool:
        """Compose email draft and save output file.

        Returns:
            bool: True on success, False on failure.
        """
        self.logger.info(f"draft_email composing to: '{recipient}', subject: '{subject}'")
        try:
            os.makedirs(os.path.dirname(os.path.abspath(export_path)), exist_ok=True)
            with open(export_path, "w", encoding="utf-8") as f:
                f.write(f"To: {recipient}\n")
                f.write(f"Subject: {subject}\n")
                f.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 40 + "\n")
                f.write(body + "\n")

            self.logger.info(f"Email draft written successfully to: '{export_path}'")
            return True
        except Exception as e:
            self.logger.error(f"Exception raised in draft_email: {e}")
            return False

    def archive_reports(self, directory_path: str, archive_name: str) -> bool:
        """Archive generated documents into a zip file package.

        Returns:
            bool: True on success, False on failure.
        """
        self.logger.info(
            f"archive_reports packing directory '{directory_path}' into '{archive_name}'"
        )
        if not os.path.exists(directory_path):
            self.logger.error(f"archive_reports failed: directory '{directory_path}' does not exist.")
            return False

        try:
            os.makedirs(os.path.dirname(os.path.abspath(archive_name)), exist_ok=True)
            with zipfile.ZipFile(archive_name, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for root, dirs, files in os.walk(directory_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        if os.path.abspath(file_path) == os.path.abspath(archive_name):
                            continue
                        arcname = os.path.relpath(file_path, directory_path)
                        zip_file.write(file_path, arcname)

            self.logger.info(f"Directory successfully compressed to archive: '{archive_name}'")
            return True
        except Exception as e:
            self.logger.error(f"Exception raised in archive_reports: {e}")
            return False
