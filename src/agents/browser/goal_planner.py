"""Goal Planner implementation – transforms a high‑level Goal into a concrete GoalPlan.

The planner is deliberately lightweight and **does not** generate any browser selectors or Playwright code. It operates purely on semantic information and produces a list of logical ``GoalStep`` objects that downstream agents can consume.
"""

from __future__ import annotations

import uuid
from datetime import timedelta
from typing import Dict, List, Any

from .goal_models import Goal, GoalStep, GoalPlan, GoalAction, GoalConstraint, to_json
from .goal_validator import GoalValidator

# ---------------------------------------------------------------------------
# Template definition
# ---------------------------------------------------------------------------

class GoalStepTemplate:
    """Simple container for a step template.

    ``action`` – GoalAction enum value.
    ``parameters`` – dict with placeholder strings ``{entity_name}`` that will be
    formatted using the ``Goal.entities`` mapping.
    ``description`` – human readable description (optional). ``optional`` – flag
    indicating whether the step can be omitted if required placeholders are
    missing.
    """

    def __init__(self, action: GoalAction, parameters: Dict[str, str] | None = None,
                 description: str = "", optional: bool = False):
        self.action = action
        self.parameters = parameters or {}
        self.description = description
        self.optional = optional

    def instantiate(self, goal: Goal) -> GoalStep | None:
        """Instantiate the template for a given ``Goal``.

        Returns ``GoalStep`` if all placeholders can be resolved, otherwise ``None``
        (the step will be omitted). When the step is optional the caller may decide
        to keep or drop it; the planner drops it and reduces confidence.
        """
        filled_params: Dict[str, Any] = {}
        for key, tmpl in self.parameters.items():
            try:
                filled_params[key] = tmpl.format(**goal.entities)
            except KeyError:
                # Required placeholder missing.
                return None
        # Order is filled later by the planner.
        return GoalStep(
            order=0,  # placeholder, will be overwritten by planner ordering
            action=self.action,
            parameters=filled_params,
            description=self.description,
            depends_on=[],
            optional=self.optional,
        )

# ---------------------------------------------------------------------------
# Template library – extendable without code changes.
# ---------------------------------------------------------------------------

STEP_TEMPLATES: Dict[str, List[GoalStepTemplate]] = {
    "search": [
        GoalStepTemplate(
            action=GoalAction.NAVIGATE,
            parameters={"domain": "google.com", "query": "{query}"},
            description="Navigate to search page",
        ),
        GoalStepTemplate(
            action=GoalAction.ENTER_TEXT,
            parameters={"field": "search_box", "text": "{query}"},
            description="Enter search query",
        ),
        GoalStepTemplate(
            action=GoalAction.SUBMIT,
            parameters={"button": "search"},
            description="Submit search",
        ),
        GoalStepTemplate(
            action=GoalAction.WAIT_FOR_RESULTS,
            description="Wait for search results",
        ),
    ],
    "login": [
        GoalStepTemplate(
            action=GoalAction.NAVIGATE,
            parameters={"url": "{login_url}"},
            description="Navigate to login page",
        ),
        GoalStepTemplate(
            action=GoalAction.ENTER_TEXT,
            parameters={"field": "username", "text": "{username}"},
            description="Enter username",
        ),
        GoalStepTemplate(
            action=GoalAction.ENTER_TEXT,
            parameters={"field": "password", "text": "{password}"},
            description="Enter password",
        ),
        GoalStepTemplate(
            action=GoalAction.SUBMIT,
            parameters={"button": "login"},
            description="Submit login form",
        ),
    ],
    # Additional goal types can be added here.
}

# ---------------------------------------------------------------------------
# Planner implementation
# ---------------------------------------------------------------------------

class GoalPlanner:
    """Transforms a ``Goal`` into a ``GoalPlan`` using the template library.

    The planner is **stateless** and therefore safe to be instantiated once and
    reused (e.g. injected as a singleton). No browser‑specific logic is present.
    """

    def __init__(self, templates: Dict[str, List[GoalStepTemplate]] | None = None, validator: GoalValidator | None = None):
        self.templates = templates if templates is not None else STEP_TEMPLATES
        self.validator = validator if validator is not None else GoalValidator()

    def create_plan(self, goal: Goal) -> GoalPlan:
        # Validate goal first
        self.validator.validate(goal)

        if goal.type not in self.templates:
            raise ValueError(f"Unsupported goal type: {goal.type}")

        raw_templates = self.templates[goal.type]
        steps: List[GoalStep] = []
        confidence: float = 1.0
        order_counter = 1

        for tmpl in raw_templates:
            step = tmpl.instantiate(goal)
            if step is None:
                # Placeholder missing – reduce confidence and skip optional steps.
                confidence *= 0.8
                if tmpl.optional:
                    continue
                else:
                    # Required step missing – we still include a placeholder step
                    # with empty parameters to keep ordering but mark it optional.
                    step = GoalStep(
                        order=order_counter,
                        action=tmpl.action,
                        parameters={},
                        description=tmpl.description,
                        depends_on=[],
                        optional=True,
                    )
            # Assign correct order now.
            step = GoalStep(
                order=order_counter,
                action=step.action,
                parameters=step.parameters,
                description=step.description,
                depends_on=step.depends_on,
                optional=step.optional,
            )
            steps.append(step)
            order_counter += 1

        # Estimate duration – naive linear model: 5 seconds per step.
        estimated_duration = timedelta(seconds=5 * len(steps))

        plan = GoalPlan(
            goal_id=goal.id,
            steps=steps,
            confidence=round(confidence, 3),
            estimated_duration=estimated_duration,
            metadata={"planner": "GoalPlanner", "template_version": "v1"},
        )
        return plan

# ---------------------------------------------------------------------------
# Exported convenience function
# ---------------------------------------------------------------------------

def create_plan(goal: Goal) -> GoalPlan:
    """Helper that creates a planner instance and returns a plan.

    This function mirrors the simple public API used by the rest of the system.
    """
    planner = GoalPlanner()
    return planner.create_plan(goal)


"""Example usage (not executed in production):

    from src.agents.browser.goal_models import Goal
    goal = Goal(type="search", entities={"domain": "example.com", "query": "test"})
    plan = create_plan(goal)
    print(to_json(plan))
"""
