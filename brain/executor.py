"""
brain/executor.py
-----------------
Executes the task plan from the planner.
Calls router for each task, collects results.
"""

from brain.router import route_task
from memory.memory_db import save_task


def execute_plan(plan: dict) -> str:
    """
    Execute a task plan (output of planner.plan_task).
    
    Args:
        plan: dict with 'tasks' list and 'summary'
    
    Returns:
        Final combined result string for the user.
    """
    tasks   = plan.get("tasks", [])
    summary = plan.get("summary", "")

    if not tasks:
        return "No tasks to execute."

    results = []

    for task in tasks:
        task_id   = task.get("id", "?")
        action    = task.get("action", "unknown")
        desc      = task.get("description", "")

        print(f"[Executor] Running task {task_id}: {action} — {desc}")

        try:
            result = route_task(task)
            save_task(f"{action}: {desc}", "success", result[:200])
        except Exception as e:
            result = f"⚠️ Task failed: {e}"
            save_task(f"{action}: {desc}", "error", str(e))
            print(f"[Executor] Task {task_id} error: {e}")

        results.append(result)

    # If only one task, return its result directly
    if len(results) == 1:
        return results[0]

    # Multiple results: join with separators
    combined = []
    for i, (task, result) in enumerate(zip(tasks, results)):
        combined.append(f"── Step {i+1}: {task.get('description', '')} ──")
        combined.append(result)
        combined.append("")

    return "\n".join(combined).strip()