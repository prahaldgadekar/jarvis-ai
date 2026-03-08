"""
tools/search_tools.py
---------------------
File search and system search tools for JARVIS.
"""

import os
import fnmatch
from pathlib import Path


def search_files(
    query: str,
    search_dir: str = None,
    extensions: list = None,
    max_results: int = 20
) -> list:
    """
    Search for files by name or partial name.
    
    Args:
        query       : filename or keyword to search
        search_dir  : directory to search (default: user home)
        extensions  : list of extensions to filter e.g. ['.py', '.java']
        max_results : max number of results to return
    
    Returns:
        list of matching file paths
    """
    if search_dir is None:
        search_dir = str(Path.home())

    results = []
    query_lower = query.lower()

    # Skip these directories to avoid long searches
    skip_dirs = {".git", "node_modules", "__pycache__", ".venv", "venv", ".idea"}

    for root, dirs, files in os.walk(search_dir):
        # Remove skipped dirs in-place
        dirs[:] = [d for d in dirs if d not in skip_dirs]

        for filename in files:
            if query_lower in filename.lower():
                if extensions:
                    if not any(filename.endswith(ext) for ext in extensions):
                        continue
                results.append(os.path.join(root, filename))
                if len(results) >= max_results:
                    return results

    return results


def search_files_by_extension(ext: str, search_dir: str = None, max_results: int = 30) -> list:
    """Find all files with a specific extension."""
    if not ext.startswith("."):
        ext = "." + ext
    if search_dir is None:
        search_dir = str(Path.home())
    return search_files("", search_dir, [ext], max_results)


def read_file(path: str) -> str:
    """Read and return file contents."""
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        return f"[ERROR] Cannot read file: {e}"


def get_directory_tree(path: str, max_depth: int = 3, indent: int = 0) -> str:
    """Return a formatted directory tree."""
    if indent > max_depth:
        return ""
    
    lines = []
    prefix = "  " * indent

    try:
        entries = sorted(os.listdir(path))
    except PermissionError:
        return f"{prefix}[Permission Denied]"

    for entry in entries:
        if entry.startswith("."):
            continue
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            lines.append(f"{prefix}📁 {entry}/")
            lines.append(get_directory_tree(full_path, max_depth, indent + 1))
        else:
            lines.append(f"{prefix}📄 {entry}")

    return "\n".join(lines)


def format_search_results(results: list) -> str:
    if not results:
        return "No files found."
    output = f"Found {len(results)} file(s):\n"
    for i, path in enumerate(results, 1):
        output += f"  {i}. {path}\n"
    return output.strip()


# ── Tool registry entry ───────────────────────────────────────

SEARCH_TOOLS = {
    "search_file": {
        "description": "Search for a file by name on the computer",
        "function": lambda query: format_search_results(search_files(query)),
    },
    "read_file": {
        "description": "Read the contents of a file at a given path",
        "function": read_file,
    },
    "directory_tree": {
        "description": "Show directory tree of a folder",
        "function": lambda path: get_directory_tree(path),
    },
}