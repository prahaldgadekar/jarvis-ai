"""
brain/planner.py
----------------
Task decomposition and structured planning using the reasoning LLM.
Breaks complex commands into step-by-step task lists.
"""

import json
from models.llm_interface import call_reasoning_model


PLANNER_SYSTEM_PROMPT = """You are JARVIS's task planner. Your job is to break down a user request into a list of clear, executable steps.

Output ONLY a JSON object in this format:
{
  "tasks": [
    {"id": 1, "action": "tool_or_action_name", "description": "what to do", "params": {}},
    {"id": 2, "action": "llm_response", "description": "generate a response about X", "params": {}}
  ],
  "summary": "Brief one-line plan summary"
}

Available actions:
- get_weather         → params: {city: "..."}
- get_news            → params: {category: "technology", count: 5}
- get_system_status   → params: {}
- search_file         → params: {query: "filename"}
- create_java_project → params: {name: "ProjectName"}
- create_c_project    → params: {name: "ProjectName"}
- create_cpp_project  → params: {name: "ProjectName"}
- create_python_project → params: {name: "ProjectName"}
- list_projects       → params: {}
- llm_response        → params: {prompt: "...", model: "reasoning|coding"}
- remember_preference → params: {key: "...", value: "..."}
- open_app            → params: {app: "appname"}

Keep tasks minimal. 1-3 tasks for simple requests, up to 6 for complex ones.
"""


def plan_task(user_input: str, context: list = None) -> dict:
    """
    Takes user input and returns a structured task plan.
    
    Returns:
        dict with 'tasks' list and 'summary' string
    """
    context_str = ""
    if context:
        context_str = "\nRecent conversation:\n" + "\n".join(
            f"{m['role'].upper()}: {m['content']}" for m in context[-4:]
        )

    prompt = f"{context_str}\n\nUser request: {user_input}\n\nCreate a task plan:"

    response = call_reasoning_model(prompt, system=PLANNER_SYSTEM_PROMPT)

    # Try to parse JSON from response
    try:
        # Strip any markdown code fences
        clean = response.strip()
        if clean.startswith("```"):
            clean = clean.split("```")[1]
            if clean.startswith("json"):
                clean = clean[4:]
        plan = json.loads(clean.strip())
        return plan
    except Exception:
        # Fallback: single LLM response task
        print(f"[Planner] Could not parse JSON plan, using fallback.\nRaw: {response[:200]}")
        return {
            "tasks": [
                {
                    "id": 1,
                    "action": "llm_response",
                    "description": "Answer the user request",
                    "params": {"prompt": user_input, "model": "reasoning"}
                }
            ],
            "summary": "Direct LLM response"
        }