"""
RAYZEN AI
System Demo Runner

Version : 0.1.0
"""

from src.core.app import RayzenApp


def main():
    print("=" * 60)
    print("RAYZEN AI - System Demo Runner")
    print("=" * 60)

    app = RayzenApp()

    # Test 1: Desktop application opening via legacy / CommandEngine logic
    print("\n--- Test 1: Simulating Desktop App Open Intent ---")
    app.command_engine.execute("open calculator")

    # Test 2: Excel analysis mapping via TaskPlanner & WorkflowEngine
    print("\n--- Test 2: Simulating Excel Analysis Planner ---")
    plan = app.task_planner.create_plan("analyze data/reports.xlsx")
    print(f"Generated Plan Steps: {plan}")

    # Test 3: Generic Browser Workflow execution
    print("\n--- Test 3: Running Workflow Engine ---")
    success = app.workflow_engine.execute("Download latest electricity bill")
    print(f"Workflow execution success: {success}")

    print("\n" + "=" * 60)
    print("Demo Execution Completed Successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
