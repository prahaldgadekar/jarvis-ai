"""
tools/project_tools.py
----------------------
Project generator: creates Java, C, C++, Python project structures.
"""

import os
import subprocess
from pathlib import Path


PROJECTS_ROOT = str(Path.home() / "JarvisProjects")


def ensure_projects_root():
    os.makedirs(PROJECTS_ROOT, exist_ok=True)


def create_java_project(project_name: str) -> str:
    """Create a basic Java project structure."""
    ensure_projects_root()
    base = os.path.join(PROJECTS_ROOT, project_name)
    src  = os.path.join(base, "src", "main", "java")
    test = os.path.join(base, "src", "test", "java")

    os.makedirs(src,  exist_ok=True)
    os.makedirs(test, exist_ok=True)

    # Main.java
    main_java = os.path.join(src, "Main.java")
    with open(main_java, "w") as f:
        f.write(f"""public class Main {{
    public static void main(String[] args) {{
        System.out.println("Hello from {project_name}!");
    }}
}}
""")

    # build.gradle (simple)
    with open(os.path.join(base, "build.gradle"), "w") as f:
        f.write("""plugins {
    id 'java'
}

repositories {
    mavenCentral()
}

dependencies {
    testImplementation 'junit:junit:4.13.2'
}
""")

    # README
    with open(os.path.join(base, "README.md"), "w") as f:
        f.write(f"# {project_name}\n\nCreated by JARVIS.\n")

    return f"✅ Java project '{project_name}' created at:\n{base}"


def create_c_project(project_name: str) -> str:
    """Create a basic C project structure."""
    ensure_projects_root()
    base = os.path.join(PROJECTS_ROOT, project_name)
    src  = os.path.join(base, "src")
    inc  = os.path.join(base, "include")
    obj  = os.path.join(base, "obj")

    for d in [src, inc, obj]:
        os.makedirs(d, exist_ok=True)

    with open(os.path.join(src, "main.c"), "w") as f:
        f.write(f"""#include <stdio.h>

int main() {{
    printf("Hello from {project_name}!\\n");
    return 0;
}}
""")

    with open(os.path.join(base, "Makefile"), "w") as f:
        f.write(f"""CC = gcc
CFLAGS = -Wall -I./include
SRC = src/main.c
OUT = {project_name.lower()}

all:
\t$(CC) $(CFLAGS) $(SRC) -o $(OUT)

clean:
\trm -f $(OUT) obj/*.o
""")

    with open(os.path.join(base, "README.md"), "w") as f:
        f.write(f"# {project_name}\n\nCreated by JARVIS.\n\n## Build\n\n```\nmake\n```\n")

    return f"✅ C project '{project_name}' created at:\n{base}"


def create_cpp_project(project_name: str) -> str:
    """Create a basic C++ project structure."""
    ensure_projects_root()
    base = os.path.join(PROJECTS_ROOT, project_name)
    src  = os.path.join(base, "src")
    inc  = os.path.join(base, "include")

    for d in [src, inc]:
        os.makedirs(d, exist_ok=True)

    with open(os.path.join(src, "main.cpp"), "w") as f:
        f.write(f"""#include <iostream>

int main() {{
    std::cout << "Hello from {project_name}!" << std::endl;
    return 0;
}}
""")

    with open(os.path.join(base, "CMakeLists.txt"), "w") as f:
        f.write(f"""cmake_minimum_required(VERSION 3.10)
project({project_name})
set(CMAKE_CXX_STANDARD 17)
add_executable({project_name.lower()} src/main.cpp)
""")

    with open(os.path.join(base, "README.md"), "w") as f:
        f.write(f"# {project_name}\n\nCreated by JARVIS.\n\n## Build\n\n```\ncmake . && make\n```\n")

    return f"✅ C++ project '{project_name}' created at:\n{base}"


def create_python_project(project_name: str) -> str:
    """Create a basic Python project structure."""
    ensure_projects_root()
    snake = project_name.lower().replace(" ", "_").replace("-", "_")
    base  = os.path.join(PROJECTS_ROOT, project_name)
    pkg   = os.path.join(base, snake)
    tests = os.path.join(base, "tests")

    for d in [pkg, tests]:
        os.makedirs(d, exist_ok=True)

    with open(os.path.join(pkg, "__init__.py"), "w") as f:
        f.write(f'"""Package: {project_name}"""\n')

    with open(os.path.join(pkg, "main.py"), "w") as f:
        f.write(f"""def main():
    print("Hello from {project_name}!")

if __name__ == "__main__":
    main()
""")

    with open(os.path.join(base, "requirements.txt"), "w") as f:
        f.write("# Add your dependencies here\n")

    with open(os.path.join(base, "README.md"), "w") as f:
        f.write(f"# {project_name}\n\nCreated by JARVIS.\n")

    return f"✅ Python project '{project_name}' created at:\n{base}"


def open_project_in_vscode(project_path: str) -> str:
    """Open a project folder in VS Code."""
    try:
        subprocess.Popen(["code", project_path])
        return f"✅ Opened in VS Code: {project_path}"
    except FileNotFoundError:
        return "[ERROR] VS Code (code) not found in PATH."


def list_projects() -> str:
    ensure_projects_root()
    projects = os.listdir(PROJECTS_ROOT)
    if not projects:
        return "No projects found."
    return "📁 Your projects:\n" + "\n".join(f"  - {p}" for p in sorted(projects))


# ── Tool registry entry ───────────────────────────────────────

PROJECT_TOOLS = {
    "create_java_project": {
        "description": "Create a new Java project",
        "function": create_java_project,
    },
    "create_c_project": {
        "description": "Create a new C project",
        "function": create_c_project,
    },
    "create_cpp_project": {
        "description": "Create a new C++ project",
        "function": create_cpp_project,
    },
    "create_python_project": {
        "description": "Create a new Python project",
        "function": create_python_project,
    },
    "list_projects": {
        "description": "List all JARVIS-created projects",
        "function": list_projects,
    },
}