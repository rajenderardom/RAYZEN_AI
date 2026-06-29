"""
RAYZEN AI
Office Agent History

Version : 0.1.0
"""

import threading
from typing import List
from src.agents.office.office_models import TaskRecord


class OfficeHistory:
    """Manages thread-safe auditing history of all tasks processed by the Office Agent."""

    def __init__(self):
        self._lock = threading.Lock()
        self._records: List[TaskRecord] = []

    def add_record(self, record: TaskRecord) -> None:
        with self._lock:
            self._records.append(record)

    def get_all_records(self) -> List[TaskRecord]:
        with self._lock:
            return list(self._records)

    def clear(self) -> None:
        with self._lock:
            self._records.clear()
