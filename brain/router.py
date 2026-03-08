"""
brain/router.py - COMPLETE CLEAN FILE
Handles all tool routing including all APIs.
"""
import time
from models.llm_interface import call_reasoning_model, call_coding_model, is_ollama_running

JARVIS_SYSTEM = """You are JARVIS. Answer in maximum 2 short plain sentences.
Never use any symbols like star, hash, backtick, slash, bracket.
Never repeat rules. Never explain yourself. Just answer directly.
Call the user Boss sometimes."""

TOOL_ACTIONS = {
    "get_weather","get_news","get_system_status",
    "search_file","read_file","directory_tree",
    "create_java_project","create_c_project","create_cpp_project",
    "create_python_project","list_projects",
    "remember_preference","get_preferences",
    "create_desktop_file","create_desktop_folder",
    "list_desktop","delete_desktop_file","open_app",
    "get_crypto","get_top_crypto","get_joke",
    "get_nasa","get_ip_info","get_exchange",
    "wiki_search","get_github",
}


def route_task(task: dict) -> str:
    action = task.get("action", "llm_response")
    params = task.get("params", {})

    if action in TOOL_ACTIONS:
        return _run_tool(action, params)

    if action == "llm_response":
        prompt = params.get("prompt", task.get("description", ""))
        model  = params.get("model", "reasoning")
        return _run_llm(prompt, model)

    return _run_llm(task.get("description", ""), "reasoning")


def _run_llm(prompt: str, model: str = "reasoning") -> str:
    for attempt in range(5):
        if is_ollama_running(retries=1, wait=0):
            break
        wait = 3 if attempt < 3 else 6
        print(f"[Router] Waiting for Ollama {wait}s (try {attempt+1}/5)...")
        time.sleep(wait)
    else:
        return "Ollama is not running. Please launch JARVIS using START_JARVIS.bat"

    if model == "coding" or _is_code(prompt):
        return call_coding_model(prompt, system=JARVIS_SYSTEM)
    return call_reasoning_model(prompt, system=JARVIS_SYSTEM)


def _is_code(prompt: str) -> bool:
    keywords = ["write code","generate code","function","class","implement",
                "debug","fix code","script","program","java","python",
                "c++","html","css","sql","algorithm"]
    return any(k in prompt.lower() for k in keywords)


def _run_tool(action: str, params: dict) -> str:

    # ── Weather ───────────────────────────────────────────────
    if action == "get_weather":
        from api.weather import format_weather
        return format_weather(params.get("city"))

    # ── News ──────────────────────────────────────────────────
    if action == "get_news":
        from api.news import format_news
        return format_news(params.get("category","technology"), params.get("count",5))

    # ── System ────────────────────────────────────────────────
    if action == "get_system_status":
        from tools.system_tools import get_system_summary
        return get_system_summary()

    # ── Wikipedia ─────────────────────────────────────────────
    if action == "wiki_search":
        from api.extras import search_wikipedia
        return search_wikipedia(params.get("query",""))

    # ── Crypto ────────────────────────────────────────────────
    if action == "get_crypto":
        from api.extras import get_crypto_price
        return get_crypto_price(params.get("coin","bitcoin"))

    if action == "get_top_crypto":
        from api.extras import get_top_crypto
        return get_top_crypto()

    # ── Joke ──────────────────────────────────────────────────
    if action == "get_joke":
        from api.extras import get_joke
        return get_joke()

    # ── NASA ──────────────────────────────────────────────────
    if action == "get_nasa":
        from api.extras import get_nasa_apod
        return get_nasa_apod()

    # ── IP info ───────────────────────────────────────────────
    if action == "get_ip_info":
        from api.extras import get_my_ip_info
        return get_my_ip_info()

    # ── Currency exchange ─────────────────────────────────────
    if action == "get_exchange":
        from api.extras import get_exchange_rate
        return get_exchange_rate(params.get("from","USD"), params.get("to","INR"))

    # ── GitHub ────────────────────────────────────────────────
    if action == "get_github":
        from api.extras import get_github_profile
        username = params.get("username","")
        if not username:
            return "Please tell me the GitHub username Boss."
        return get_github_profile(username)

    # ── File search ───────────────────────────────────────────
    if action == "search_file":
        from tools.search_tools import search_files, format_search_results
        return format_search_results(search_files(params.get("query","")))

    if action == "read_file":
        from tools.search_tools import read_file
        return read_file(params.get("path",""))

    if action == "directory_tree":
        from tools.search_tools import get_directory_tree
        return get_directory_tree(params.get("path","."))

    # ── Projects ──────────────────────────────────────────────
    if action == "create_java_project":
        from tools.project_tools import create_java_project
        return create_java_project(params.get("name","MyProject"))

    if action == "create_c_project":
        from tools.project_tools import create_c_project
        return create_c_project(params.get("name","MyProject"))

    if action == "create_cpp_project":
        from tools.project_tools import create_cpp_project
        return create_cpp_project(params.get("name","MyProject"))

    if action == "create_python_project":
        from tools.project_tools import create_python_project
        return create_python_project(params.get("name","MyProject"))

    if action == "list_projects":
        from tools.project_tools import list_projects
        return list_projects()

    # ── Memory ────────────────────────────────────────────────
    if action == "remember_preference":
        from memory.memory_db import set_preference
        key = params.get("key","")
        val = params.get("value","")
        if key:
            set_preference(key, val)
            return "Got it Boss. I will remember that."
        return "No key provided."

    if action == "get_preferences":
        from memory.memory_db import get_all_preferences
        prefs = get_all_preferences()
        if not prefs:
            return "No preferences saved yet."
        return "Your preferences: " + ", ".join(f"{k} is {v}" for k,v in prefs.items())

    # ── Desktop tools ─────────────────────────────────────────
    if action == "create_desktop_file":
        from tools.windows_tools import create_file_on_desktop
        return create_file_on_desktop(params.get("filename","file.txt"), params.get("content",""))

    if action == "create_desktop_folder":
        from tools.windows_tools import create_folder_on_desktop
        return create_folder_on_desktop(params.get("foldername","NewFolder"))

    if action == "list_desktop":
        from tools.windows_tools import list_desktop_files
        return list_desktop_files()

    if action == "delete_desktop_file":
        from tools.windows_tools import delete_file_on_desktop
        return delete_file_on_desktop(params.get("filename",""))

    if action == "open_app":
        from tools.windows_tools import open_application
        return open_application(params.get("app",""))

    return f"Tool {action} not implemented yet."