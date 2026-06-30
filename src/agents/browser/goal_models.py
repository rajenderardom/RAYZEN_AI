"""Goal Planning Data Models for RAYZEN AI.

This module defines the core immutable data structures used by the Goal Planner.
All models are plain dataclasses and therefore JSON‑serialisable via ``dataclasses.asdict``
or by passing a ``default=str`` function to ``json.dumps`` (which handles ``Enum``, ``datetime``
and ``UUID`` objects).
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List


class GoalAction(Enum):
    """Canonical actions that a GoalPlanner can emit.

    The enum is deliberately small – downstream agents map these actions to concrete
    implementations (e.g. BrowserAgent.navigate, BrowserAgent.enter_text, etc.).
    """

    NAVIGATE = "navigate"
    AUTHENTICATE = "authenticate"
    ENTER_TEXT = "enter_text"
    CLICK = "click"
    SUBMIT = "submit"
    WAIT_FOR_RESULTS = "wait_for_results"
    EXTRACT = "extract"
    FILTER = "filter"
    # Extend as needed without changing existing semantics.


@dataclass(frozen=True)
class GoalConstraint:
    """Simple name/value constraint supplied by the user.

    Example: ``GoalConstraint(name="max_price", value=500)``.
    """

    name: str
    value: Any


@dataclass(frozen=True)
class Goal:
    """High‑level user intent extracted from natural language.

    ``type`` is a coarse categorisation (e.g. ``search``, ``book``).
    ``entities`` holds the extracted semantic entities (e.g. ``{"destination": "Tokyo"}``).
    ``constraints`` is a list of optional ``GoalConstraint`` objects.
    """

    id: uuid.UUID = field(default_factory=uuid.uuid4)
    type: str = ""
    entities: Dict[str, Any] = field(default_factory=dict)
    constraints: List[GoalConstraint] = field(default_factory=list)


@dataclass(frozen=True)
class GoalStep:
    """A single logical step within a ``GoalPlan``.

    ``order`` determines execution ordering. ``depends_on`` can be used to express
    DAG relationships – it is a list of lower‑order step ``order`` values.
    ``optional`` marks steps that can be omitted without failing the whole plan.
    """

    order: int
    action: GoalAction
    parameters: Dict[str, Any] = field(default_factory=dict)
    description: str = ""
    depends_on: List[int] = field(default_factory=list)
    optional: bool = False


@dataclass(frozen=True)
class GoalPlan:
    """A complete, ordered plan derived from a ``Goal``.

    ``confidence`` expresses the planner's certainty (0‑1). ``estimated_duration``
    is a rough execution time estimate. ``metadata`` can store arbitrary key/value
    pairs for provenance or tracing purposes.
    """

    goal_id: uuid.UUID
    steps: List[GoalStep] = field(default_factory=list)
    confidence: float = 1.0
    estimated_duration: timedelta = field(default_factory=timedelta)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass(frozen=True)
class GoalResult:
    """Result of executing a ``GoalPlan``.

    ``outputs`` holds high‑level structured data produced by the workflow.
    ``artifacts`` can contain URIs or file paths to generated assets.
    ``errors`` is a list of error messages or structured error objects.
    """

    plan_id: uuid.UUID
    status: str  # e.g. "SUCCESS", "PARTIAL", "FAILURE"
    outputs: Dict[str, Any] = field(default_factory=dict)
    artifacts: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    completed_at: datetime = field(default_factory=datetime.utcnow)


def to_json(obj: Any) -> str:
    """Serialises a dataclass instance (or a collection of them) to JSON.

    Enums are serialised by their value, and other custom objects like UUIDs and
    datetimes/timedeltas are serialised as strings.
    """
    import json

    def custom_serializer(val: Any) -> Any:
        if isinstance(val, Enum):
            return val.value
        return str(val)

    if isinstance(obj, (list, tuple)):
        data = [asdict(item) if hasattr(item, "__dataclass_fields__") else item for item in obj]
    elif hasattr(obj, "__dataclass_fields__"):
        data = asdict(obj)
    else:
        data = obj

    return json.dumps(data, default=custom_serializer, ensure_ascii=False, indent=2)

