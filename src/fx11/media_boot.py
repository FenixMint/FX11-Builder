from __future__ import annotations

from dataclasses import dataclass

from .gparted import GPARTED_LIVE
from .iso import BuilderError


FX11_MANIFEST_PATH = "/FX11-manifest.json"
WINDOWS_MEDIA_BOOT_PATH = "/bootmgr.efi"
GPARTED_LOCALE = "pl_PL.UTF-8"
GPARTED_KEYBOARD_LAYOUT = "pl"


@dataclass(frozen=True)
class MediaBootConfig:
    grub_config: str
    gparted_iso_path: str
    windows_boot_path: str


def _escape_grub_single(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'")


def gparted_iso_path() -> str:
    return f"/FX11/gparted/{GPARTED_LIVE.filename}"


def build_media_grub_config(
    *,
    timeout_seconds: int = 5,
    default_entry: str = "fx-partition-manager",
    windows_boot_path: str = WINDOWS_MEDIA_BOOT_PATH,
    gparted_locale: str = GPARTED_LOCALE,
    gparted_keyboard_layout: str = GPARTED_KEYBOARD_LAYOUT,
) -> MediaBootConfig:
    if timeout_seconds < 0:
        raise BuilderError("FX11 installation-media boot timeout cannot be negative.")
    if not windows_boot_path.startswith("/"):
        raise BuilderError("Windows media boot path must be an absolute GRUB filesystem path.")
    if not gparted_locale.strip():
        raise BuilderError("GParted locale cannot be empty.")
    if not gparted_keyboard_layout.strip():
        raise BuilderError("GParted keyboard layout cannot be empty.")

    gparted_path = gparted_iso_path()
    escaped_gparted = _escape_grub_single(gparted_path)
    escaped_windows = _escape_grub_single(windows_boot_path)
    escaped_default = _escape_grub_single(default_entry)
    escaped_locale = _escape_grub_single(gparted_locale)
    escaped_keyboard = _escape_grub_single(gparted_keyboard_layout)

    lines = [
        "insmod part_gpt",
        "insmod fat",
        "insmod iso9660",
        "insmod search",
        "insmod search_file",
        "insmod loopback",
        "insmod chain",
        f"set timeout={timeout_seconds}",
        f"set default='{escaped_default}'",
        "",
        "menuentry 'FX Partition Manager — powered by GParted' --id 'fx-partition-manager' {",
        f"  search --no-floppy --file --set=fxmedia {FX11_MANIFEST_PATH}",
        f"  set isofile='{escaped_gparted}'",
        "  loopback loop ($fxmedia)$isofile",
        (
            "  linux (loop)/live/vmlinuz boot=live config union=overlay username=user components "
            "noswap noeject ip= net.ifnames=0 "
            f"locales={escaped_locale} keyboard-layouts={escaped_keyboard} gl_batch "
            "toram=filesystem.squashfs findiso=$isofile"
        ),
        "  initrd (loop)/live/initrd.img",
        "}",
        "",
        "menuentry 'FX11 Installer / WinPE fallback' --id 'fx11-winpe' {",
        f"  search --no-floppy --file --set=winmedia {escaped_windows}",
        f"  chainloader ($winmedia){escaped_windows}",
        "}",
        "",
        "menuentry 'UEFI Firmware Settings' --id 'uefi-firmware' {",
        "  fwsetup",
        "}",
        "",
    ]

    return MediaBootConfig(
        grub_config="\n".join(lines),
        gparted_iso_path=gparted_path,
        windows_boot_path=windows_boot_path,
    )
