"""
tools/windows_tools.py - Real Windows Desktop actions
"""
import os
import subprocess


def get_desktop() -> str:
    # Best method: User Shell Folders registry key (handles OneDrive)
    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
        )
        desktop, _ = winreg.QueryValueEx(key, "Desktop")
        winreg.CloseKey(key)
        desktop = os.path.expandvars(desktop)
        if os.path.exists(desktop):
            print(f"[Desktop] {desktop}")
            return desktop
    except Exception as e:
        print(f"[Desktop] Registry error: {e}")

    # Fallback: OneDrive Desktop
    for env_var in ["OneDriveConsumer", "OneDrive"]:
        base = os.environ.get(env_var, "")
        if base:
            path = os.path.join(base, "Desktop")
            if os.path.exists(path):
                print(f"[Desktop] OneDrive: {path}")
                return path

    # Fallback: USERPROFILE
    base = os.environ.get("USERPROFILE", os.path.expanduser("~"))
    path = os.path.join(base, "Desktop")
    os.makedirs(path, exist_ok=True)
    print(f"[Desktop] Fallback: {path}")
    return path


def create_file_on_desktop(filename: str, content: str = "") -> str:
    if "." not in filename:
        filename += ".txt"
    desktop = get_desktop()
    path    = os.path.join(desktop, filename)
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        if os.path.exists(path):
            return f"Done Boss. File {filename} created at {path}"
        return f"Error: file not found after writing at {path}"
    except PermissionError:
        return f"Permission denied writing to {path}"
    except Exception as e:
        return f"Failed: {e}. Path tried: {path}"


def create_folder_on_desktop(foldername: str) -> str:
    desktop = get_desktop()
    path    = os.path.join(desktop, foldername)
    try:
        os.makedirs(path, exist_ok=True)
        return f"Done Boss. Folder {foldername} created at {path}"
    except Exception as e:
        return f"Failed: {e}"


def list_desktop_files() -> str:
    desktop = get_desktop()
    try:
        files = sorted(os.listdir(desktop))
        if not files:
            return f"Desktop is empty. Path: {desktop}"
        return f"Desktop files at {desktop}:\n" + "\n".join(f"  {f}" for f in files)
    except Exception as e:
        return f"Could not read Desktop: {e}"


def delete_file_on_desktop(filename: str) -> str:
    desktop = get_desktop()
    path    = os.path.join(desktop, filename)
    if os.path.isfile(path):
        os.remove(path)
        return f"Done Boss. Deleted {filename} from Desktop."
    return f"File {filename} not found at {path}"


def open_application(app_name: str) -> str:
    known = {
        "notepad":    "notepad.exe",
        "calculator": "calc.exe",
        "paint":      "mspaint.exe",
        "explorer":   "explorer.exe",
        "chrome":     "chrome",
        "vscode":     "code",
        "cmd":        "cmd.exe",
        "eclipse":    "eclipse.exe",
    }
    exe = known.get(app_name.lower().strip(), app_name)
    try:
        subprocess.Popen(exe, shell=True)
        return f"Done Boss. Opened {app_name}."
    except Exception as e:
        return f"Could not open {app_name}: {e}"