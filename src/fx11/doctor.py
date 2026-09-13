from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import platform
import shutil


@dataclass(frozen=True)
class ToolCheck:
    name: str
    command: str
    required: bool
    found: bool
    package: str


CORE_TOOLS = (
    ("wimlib", "wimlib-imagex", "wimtools"),
    ("xorriso", "xorriso", "xorriso"),
)

OPTIONAL_TOOLS = (
    ("QEMU", "qemu-system-x86_64", "qemu-system-x86"),
    ("GRUB UEFI builder", "grub-mkstandalone", "grub-efi-amd64-bin"),
)


def detect_distribution(os_release: Path = Path("/etc/os-release")) -> tuple[str, str]:
    values: dict[str, str] = {}
    try:
        for line in os_release.read_text(encoding="utf-8").splitlines():
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key] = value.strip().strip('"')
    except OSError:
        return ("unknown", "Unknown Linux")
    return values.get("ID", "unknown"), values.get("PRETTY_NAME", "Unknown Linux")


def check_tools() -> list[ToolCheck]:
    checks: list[ToolCheck] = []
    for name, command, package in CORE_TOOLS:
        checks.append(ToolCheck(name, command, True, shutil.which(command) is not None, package))
    for name, command, package in OPTIONAL_TOOLS:
        checks.append(ToolCheck(name, command, False, shutil.which(command) is not None, package))
    return checks


def host_report() -> dict[str, object]:
    distro_id, distro_name = detect_distribution()
    tools = check_tools()
    return {
        "distribution_id": distro_id,
        "distribution": distro_name,
        "architecture": platform.machine(),
        "kernel": platform.release(),
        "tools": tools,
        "ready": all(item.found for item in tools if item.required),
    }
