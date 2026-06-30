"""Unit tests for the Goal Planner and Goal Validator.

This suite verifies that:
* GoalValidator correctly validates valid goals and raises ValueError on invalid ones.
* GoalPlanner creates ordered plans with correct actions and populated parameters.
* Model‑level helper functions function as expected.
"""

import unittest
from datetime import timedelta
from src.agents.browser.goal_models import Goal, GoalConstraint, GoalAction, GoalPlan
from src.agents.browser.goal_validator import GoalValidator
from src.agents.browser.goal_planner import GoalPlanner, create_plan

class TestGoalValidator(unittest.TestCase):
    def setUp(self):
        self.validator = GoalValidator()

    def test_valid_search_goal(self):
        goal = Goal(type="search", entities={"query": "machine learning"})
        self.assertTrue(self.validator.validate(goal))

    def test_valid_login_goal(self):
        goal = Goal(
            type="login",
            entities={
                "login_url": "https://example.com/login",
                "username": "user123",
                "password": "secure_pass",
            },
        )
        self.assertTrue(self.validator.validate(goal))

    def test_empty_goal_type(self):
        goal = Goal(type="", entities={"query": "test"})
        with self.assertRaises(ValueError) as ctx:
            self.validator.validate(goal)
        self.assertIn("Goal type must not be empty", str(ctx.exception))

    def test_unsupported_goal_type(self):
        goal = Goal(type="unsupported_action", entities={"query": "test"})
        with self.assertRaises(ValueError) as ctx:
            self.validator.validate(goal)
        self.assertIn("Unsupported goal type", str(ctx.exception))

    def test_missing_entities(self):
        goal = Goal(type="search", entities={})
        with self.assertRaises(ValueError) as ctx:
            self.validator.validate(goal)
        self.assertIn("Missing required entities", str(ctx.exception))

    def test_empty_entity_value(self):
        goal = Goal(type="search", entities={"query": "  "})
        with self.assertRaises(ValueError) as ctx:
            self.validator.validate(goal)
        self.assertIn("Required entity 'query' cannot be empty", str(ctx.exception))


class TestGoalPlanner(unittest.TestCase):
    def setUp(self):
        self.planner = GoalPlanner()

    def test_create_plan_search(self):
        goal = Goal(type="search", entities={"query": "deepmind"})
        plan = self.planner.create_plan(goal)

        self.assertIsInstance(plan, GoalPlan)
        self.assertEqual(plan.goal_id, goal.id)
        self.assertEqual(len(plan.steps), 4)
        self.assertEqual(plan.confidence, 1.0)
        self.assertEqual(plan.estimated_duration, timedelta(seconds=20))

        # Check step ordering and parameters mapping
        self.assertEqual(plan.steps[0].order, 1)
        self.assertEqual(plan.steps[0].action, GoalAction.NAVIGATE)
        self.assertEqual(plan.steps[0].parameters["query"], "deepmind")

        self.assertEqual(plan.steps[1].order, 2)
        self.assertEqual(plan.steps[1].action, GoalAction.ENTER_TEXT)
        self.assertEqual(plan.steps[1].parameters["text"], "deepmind")

        self.assertEqual(plan.steps[2].order, 3)
        self.assertEqual(plan.steps[2].action, GoalAction.SUBMIT)

    def test_create_plan_login(self):
        goal = Goal(
            type="login",
            entities={
                "login_url": "https://portal.net",
                "username": "admin",
                "password": "pwd",
            },
        )
        plan = self.planner.create_plan(goal)
        self.assertEqual(len(plan.steps), 4)
        self.assertEqual(plan.steps[0].action, GoalAction.NAVIGATE)
        self.assertEqual(plan.steps[0].parameters["url"], "https://portal.net")

        self.assertEqual(plan.steps[1].action, GoalAction.ENTER_TEXT)
        self.assertEqual(plan.steps[1].parameters["text"], "admin")

    def test_create_plan_convenience_function(self):
        goal = Goal(type="search", entities={"query": "testing helper"})
        plan = create_plan(goal)
        self.assertEqual(plan.steps[1].parameters["text"], "testing helper")

if __name__ == "__main__":
    unittest.main()
