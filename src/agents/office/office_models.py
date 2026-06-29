"""
RAYZEN AI
Office Agent Models

Version : 0.1.0
"""

import datetime
from typing import Dict, Any, Optional


class TaskRecord:
    """Represents a record of an executed task."""

    def __init__(
        self,
        task_id: str,
        description: str,
        status: str = "pending",
        started_at: Optional[datetime.datetime] = None,
        completed_at: Optional[datetime.datetime] = None,
        error_message: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.task_id = task_id
        self.description = description
        self.status = status
        self.started_at = started_at or datetime.datetime.now()
        self.completed_at = completed_at
        self.error_message = error_message
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "description": self.description,
            "status": self.status,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "error_message": self.error_message,
            "metadata": self.metadata,
        }


class AgentState:
    """Holds active execution state and properties."""

    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.current_workflow: Optional[str] = None
