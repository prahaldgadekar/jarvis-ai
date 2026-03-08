"""
tools/system_tools.py
---------------------
System monitoring tools: CPU, RAM, battery, network, disk.
"""

import psutil
import socket
import platform
from datetime import datetime


def get_cpu_usage() -> dict:
    return {
        "percent": psutil.cpu_percent(interval=1),
        "cores": psutil.cpu_count(),
        "frequency_mhz": round(psutil.cpu_freq().current, 1) if psutil.cpu_freq() else "N/A"
    }


def get_ram_usage() -> dict:
    mem = psutil.virtual_memory()
    return {
        "total_gb": round(mem.total / 1e9, 2),
        "used_gb":  round(mem.used  / 1e9, 2),
        "percent":  mem.percent
    }


def get_battery_status() -> dict:
    battery = psutil.sensors_battery()
    if battery is None:
        return {"available": False}
    return {
        "available": True,
        "percent": round(battery.percent, 1),
        "plugged_in": battery.power_plugged,
        "time_left_min": round(battery.secsleft / 60, 1) if battery.secsleft > 0 else "Charging"
    }


def get_disk_usage(path: str = "/") -> dict:
    disk = psutil.disk_usage(path)
    return {
        "total_gb": round(disk.total / 1e9, 2),
        "used_gb":  round(disk.used  / 1e9, 2),
        "free_gb":  round(disk.free  / 1e9, 2),
        "percent":  disk.percent
    }


def get_network_info() -> dict:
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        local_ip = "Unknown"
        hostname = "Unknown"
    
    net_io = psutil.net_io_counters()
    return {
        "hostname": hostname,
        "local_ip": local_ip,
        "bytes_sent_mb":  round(net_io.bytes_sent  / 1e6, 2),
        "bytes_recv_mb":  round(net_io.bytes_recv  / 1e6, 2),
    }


def get_system_summary() -> str:
    cpu  = get_cpu_usage()
    ram  = get_ram_usage()
    bat  = get_battery_status()
    disk = get_disk_usage()
    net  = get_network_info()

    lines = [
        f"System Report — {datetime.now().strftime('%H:%M:%S')}",
        f"  OS      : {platform.system()} {platform.release()}",
        f"  CPU     : {cpu['percent']}% used ({cpu['cores']} cores @ {cpu['frequency_mhz']} MHz)",
        f"  RAM     : {ram['used_gb']} / {ram['total_gb']} GB ({ram['percent']}%)",
        f"  Disk    : {disk['used_gb']} / {disk['total_gb']} GB ({disk['percent']}%)",
        f"  Network : {net['local_ip']} | ↑{net['bytes_sent_mb']} MB ↓{net['bytes_recv_mb']} MB",
    ]
    if bat["available"]:
        plug = "🔌" if bat["plugged_in"] else "🔋"
        lines.append(f"  Battery : {bat['percent']}% {plug}  Time left: {bat['time_left_min']} min")
    else:
        lines.append("  Battery : Desktop / No battery")

    return "\n".join(lines)


def get_running_processes(limit: int = 10) -> list:
    procs = []
    for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
        try:
            procs.append(p.info)
        except Exception:
            pass
    procs.sort(key=lambda x: x.get("cpu_percent", 0), reverse=True)
    return procs[:limit]


# ── Tool registry entry ───────────────────────────────────────

SYSTEM_TOOLS = {
    "get_system_status": {
        "description": "Get CPU, RAM, battery, disk, and network status",
        "function": get_system_summary,
    },
    "get_cpu": {
        "description": "Get CPU usage percentage",
        "function": lambda: get_cpu_usage(),
    },
    "get_ram": {
        "description": "Get RAM usage",
        "function": lambda: get_ram_usage(),
    },
    "get_battery": {
        "description": "Get battery status",
        "function": lambda: get_battery_status(),
    },
}