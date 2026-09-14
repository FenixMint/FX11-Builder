from __future__ import annotations

from enum import Enum
from pathlib import Path
import shlex


class LiveMode(str, Enum):
    FX11 = "windows"
    FX_LINUX = "linux"
    LIVE = "live"


CALAMARES_PROFILE_ROOT = Path("/etc/fx/calamares")


def parse_live_mode(cmdline: str) -> LiveMode | None:
    """Return the requested FX Live mode from a Linux kernel command line.

    Supported values are intentionally small and stable because GRUB, the live
    launcher and tests all share this contract.
    """

    for token in shlex.split(cmdline):
        if not token.startswith("fx.mode="):
            continue
        value = token.partition("=")[2].strip().lower()
        aliases = {
            "windows": LiveMode.FX11,
            "fx11": LiveMode.FX11,
            "linux": LiveMode.FX_LINUX,
            "fxlinux": LiveMode.FX_LINUX,
            "live": LiveMode.LIVE,
            "try": LiveMode.LIVE,
        }
        return aliases.get(value)
    return None


def calamares_profile(mode: LiveMode) -> Path | None:
    if mode == LiveMode.FX11:
        return CALAMARES_PROFILE_ROOT / "fx11"
    if mode == LiveMode.FX_LINUX:
        return CALAMARES_PROFILE_ROOT / "linux"
    return None


def calamares_command(mode: LiveMode) -> tuple[str, ...] | None:
    profile = calamares_profile(mode)
    if profile is None:
        return None
    return ("pkexec", "calamares", "-c", str(profile))
