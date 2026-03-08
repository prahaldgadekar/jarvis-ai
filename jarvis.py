"""
jarvis.py
---------
JARVIS Main Entry Point.

Usage:
    python jarvis.py          → Launch full GUI
    python jarvis.py --cli    → Command line mode (no GUI)
    python jarvis.py --check  → Check system status and dependencies
"""

import sys
import os

# Fix module path — ensures Python finds all JARVIS packages
# regardless of where the script is launched from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


def check_dependencies():
    """Check all required packages and services."""
    print("\n" + "="*55)
    print("  JARVIS — Dependency Check")
    print("="*55)

    checks = {
        "PySide6":           "PySide6",
        "SpeechRecognition": "speech_recognition",
        "pyttsx3":           "pyttsx3",
        "TextBlob":          "textblob",
        "requests":          "requests",
        "psutil":            "psutil",
        "pyautogui":         "pyautogui",
        "python-dotenv":     "dotenv",
    }

    all_ok = True
    for name, module in checks.items():
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name}  ← pip install {name.lower()}")
            all_ok = False

    # Check Ollama
    print()
    try:
        import requests as req
        resp = req.get("http://localhost:11434/api/tags", timeout=3)
        models = [m["name"] for m in resp.json().get("models", [])]
        print(f"  ✅ Ollama running  | Models: {', '.join(models) if models else 'none pulled yet'}")
        if not models:
            print("      → Pull models: ollama pull llama3.1")
            print("      → Pull models: ollama pull qwen2.5-coder")
    except Exception:
        print("  ⚠️  Ollama not running → start with: ollama serve")
        print("      Then pull models:")
        print("      ollama pull llama3.1")
        print("      ollama pull qwen2.5-coder")

    # Check .env
    print()
    if os.path.exists(".env"):
        print("  ✅ .env file found")
    else:
        print("  ⚠️  No .env file  → copy .env.example to .env and add your API keys")

    print("="*55)
    if all_ok:
        print("  All packages installed. JARVIS is ready to launch!")
    else:
        print("  Install missing packages, then run again.")
    print("="*55 + "\n")


def run_cli():
    """Simple command-line mode without GUI."""
    print("\n" + "="*50)
    print("  JARVIS — CLI Mode  (type 'exit' to quit)")
    print("="*50 + "\n")

    from brain.core import JarvisBrain
    brain = JarvisBrain()

    while True:
        try:
            user_input = input("YOU: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n[JARVIS] Goodbye.")
            break

        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit", "bye"}:
            print("[JARVIS] Goodbye!")
            break

        response = brain.process(user_input)
        print(f"\nJARVIS: {response}\n")


def run_gui():
    """Launch the full PySide6 GUI."""
    from jarvis_gui import run_gui as _run
    _run()


if __name__ == "__main__":
    args = sys.argv[1:]

    if "--check" in args:
        check_dependencies()
    elif "--cli" in args:
        run_cli()
    else:
        run_gui()