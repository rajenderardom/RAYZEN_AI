"""Unit tests for the Goal Planner data models.

These tests verify:
* Construction of each dataclass with required and optional fields.
* Enum usage for actions.
* JSON serialisation via the helper ``to_json``.
* Immutability (frozen dataclasses) – attempts to modify raise ``FrozenInstanceError``.
"""

import json
import unittest
import uuid
from datetime import timedelta, datetime
from dataclasses import FrozenInstanceError

from src.agents.browser.goal_models import (
    Goal,
    GoalConstraint,
    GoalStep,
    GoalPlan,
    GoalResult,
    GoalAction,
    to_json,
)

class TestGoalModels(unittest.TestCase):
    def test_goal_constraint(self):
        gc = GoalConstraint(name="max_price", value=500)
        self.assertEqual(gc.name, "max_price")
        self.assertEqual(gc.value, 500)
        # JSON serialisation
        json_str = to_json(gc)
        data = json.loads(json_str)
        self.assertEqual(data["name"], "max_price")
        self.assertEqual(data["value"], 500)

    def test_goal(self):
        goal = Goal(
            type="search",
            entities={"query": "cats"},
            constraints=[GoalConstraint(name="lang", value="en")],
        )
        self.assertEqual(goal.type, "search")
        self.assertIn("query", goal.entities)
        self.assertEqual(goal.constraints[0].name, "lang")
        # Frozen check
        with self.assertRaises(FrozenInstanceError):
            goal.type = "book"
        # JSON serialisation includes UUID as string
        data = json.loads(to_json(goal))
        self.assertIn("id", data)
        self.assertEqual(data["type"], "search")
        self.assertEqual(data["entities"]["query"], "cats")

    def test_goal_step(self):
        step = GoalStep(
            order=1,
            action=GoalAction.NAVIGATE,
            parameters={"url": "https://example.com"},
            description="Open homepage",
            depends_on=[],
            optional=False,
        )
        self.assertEqual(step.order, 1)
        self.assertEqual(step.action, GoalAction.NAVIGATE)
        self.assertEqual(step.parameters["url"], "https://example.com")
        # JSON serialisation – Enum becomes its value string
        data = json.loads(to_json(step))
        self.assertEqual(data["action"], "navigate")
        self.assertEqual(data["description"], "Open homepage")

    def test_goal_plan(self):
        step = GoalStep(order=1, action=GoalAction.NAVIGATE, parameters={"url": "https://example.com"})
        plan = GoalPlan(
            goal_id=uuid.uuid4(),
            steps=[step],
            confidence=0.85,
            estimated_duration=timedelta(seconds=30),
            metadata={"source": "unit_test"},
        )
        self.assertEqual(plan.confidence, 0.85)
        self.assertEqual(len(plan.steps), 1)
        # JSON serialisation – timedelta becomes ISO 8601 string via default=str
        data = json.loads(to_json(plan))
        self.assertIn("estimated_duration", data)
        self.assertEqual(data["metadata"]["source"], "unit_test")

    def test_goal_result(self):
        result = GoalResult(
            plan_id=uuid.uuid4(),
            status="SUCCESS",
            outputs={"result": "ok"},
            artifacts=["file:///tmp/report.pdf"],
            errors=[],
        )
        self.assertEqual(result.status, "SUCCESS")
        self.assertIn("result", result.outputs)
        # JSON serialisation
        data = json.loads(to_json(result))
        self.assertEqual(data["status"], "SUCCESS")
        self.assertEqual(data["artifacts"], ["file:///tmp/report.pdf"])

if __name__ == "__main__":
    unittest.main()
