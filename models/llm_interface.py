"""
models/llm_interface.py
"""

import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
REASONING_MODEL = os.getenv("REASONING_MODEL", "phi3")
CODING_MODEL    = os.getenv("CODING_MODEL",    "qwen2.5-coder:7b")
FALLBACK_MODEL  = os.getenv("FALLBACK_MODEL",  "phi3")


def _call_ollama(model: str, prompt: str, system: str = "") -> str:
    url     = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {"model": model, "prompt": prompt, "system": system, "stream": False}
    try:
        r = requests.post(url, json=payload, timeout=120)
        r.raise_for_status()
        return r.json().get("response", "").strip()
    except requests.exceptions.ConnectionError:
        return "ERROR: Cannot connect to Ollama. Use START_JARVIS.bat to launch JARVIS."
    except requests.exceptions.Timeout:
        return "ERROR: Model timed out. Try phi3 for faster responses."
    except Exception as e:
        return f"ERROR: {e}"


def call_reasoning_model(prompt: str, system: str = "") -> str:
    print(f"[LLM] Reasoning: {REASONING_MODEL}")
    return _call_ollama(REASONING_MODEL, prompt, system)


def call_coding_model(prompt: str, system: str = "") -> str:
    print(f"[LLM] Coding: {CODING_MODEL}")
    return _call_ollama(CODING_MODEL, prompt, system)


def is_ollama_running(retries: int = 3, wait: float = 2.0) -> bool:
    for i in range(retries):
        try:
            r = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=4)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        if i < retries - 1:
            print(f"[LLM] Waiting for Ollama... ({i+1}/{retries})")
            time.sleep(wait)
    return False


def list_available_models() -> list:
    try:
        r = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        return [m["name"] for m in r.json().get("models", [])]
    except Exception:
        return []