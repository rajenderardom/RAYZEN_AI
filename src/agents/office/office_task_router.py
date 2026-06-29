"""
RAYZEN AI
Office Agent Task Router

Version : 0.1.0
"""

import re
from typing import Tuple, Dict, Any, Optional
from src.core.logger import RayzenLogger


class OfficeTaskRouter:
    """Routes natural language task inputs to matched Office Agent method names and arguments."""

    def __init__(self):
        self.logger = RayzenLogger()

    def route(self, task: str) -> Tuple[Optional[str], Dict[str, Any]]:
        """Identify matching method and arguments from task description.

        Args:
            task (str): Natural language task prompt.

        Returns:
            Tuple[Optional[str], Dict[str, Any]]: Method name and parsed arguments dict.
        """
        task_lower = task.strip().lower()
        self.logger.info(f"Routing task description: '{task}'")

        # 1. Compare Excel
        if "compare" in task_lower and ("excel" in task_lower or "spreadsheet" in task_lower):
            paths = re.findall(r"[\w./-]+\.xlsx", task)
            old_file = paths[0] if len(paths) > 0 else "data/old.xlsx"
            new_file = paths[1] if len(paths) > 1 else "data/new.xlsx"

            key_col = "Site ID"
            words = task.split()
            if len(words) > 3 and not words[-1].endswith(".xlsx"):
                key_col = words[-1]

            return "compare_excel", {
                "old_file": old_file,
                "new_file": new_file,
                "key_column": key_col,
                "sheet_name": "Sheet1",
                "export_path": "data/comparison_report.xlsx",
            }

        # 2. Generate Report
        elif "report" in task_lower and ("generate" in task_lower or "create" in task_lower):
            return "generate_report", {}

        # 3. Run Workflow
        elif "workflow" in task_lower and ("run" in task_lower or "execute" in task_lower):
            json_paths = re.findall(r"[\w./-]+\.json", task)
            path = json_paths[0] if json_paths else "workflows/examples/sample_workflow.json"
            return "run_workflow", {"file_path": path}

        # 4. Draft Email
        elif "email" in task_lower and ("draft" in task_lower or "compose" in task_lower):
            recipient = "management@rayzen.ai"
            if "to " in task_lower:
                match = re.search(r"to\s+([\w.@-]+)", task, re.IGNORECASE)
                if match:
                    recipient = match.group(1)
            return "draft_email", {
                "recipient": recipient,
                "subject": "System Performance Summary",
                "body": "Hi team, Here is the latest system report.",
                "export_path": "data/email_draft.txt",
            }

        # 5. Archive Reports
        elif "archive" in task_lower or "backup" in task_lower:
            return "archive_reports", {
                "directory_path": "data",
                "archive_name": "data/archive.zip",
            }

        self.logger.warning(f"No task routing match found for query: '{task}'")
        return None, {}
