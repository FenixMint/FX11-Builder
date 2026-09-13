from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess

from .iso import BuilderError


WINDOWS_BOOT_PATH = "/EFI/Microsoft/Boot/bootmgfw.efi"
FX_GRUB_PATH = "/EFI/FX11/fxbootx64.efi"
FX_GRUB_CONFIG_PATH = "/EFI/FX11/grub.cfg"
FX_GRUB_THEME_PATH = "/EFI/FX11/theme/theme.txt"
FX_GRUB_BACKGROUND_PATH = "/EFI/FX11/theme/background.png"


@dataclass(frozen=True)
class BootEntry:
    title: str
    efi_path: str
    fs_uuid: str | None = None
    identifier: str | None = None


@dataclass(frozen=True)
class BootManagerPayload:
    efi_binary: Path
    grub_config: Path
    theme_config: Path
    secure_boot_compatible: bool


def _escape_grub(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'")


def _search_lines(entry: BootEntry, variable: str) -> list[str]:
    if entry.fs_uuid:
        return [f"search --no-floppy --fs-uuid --set={variable} {_escape_grub(entry.fs_uuid)}"]
    return [f"search --no-floppy --file --set={variable} {_escape_grub(entry.efi_path)}"]


def grub_config(
    *,
    fx11_esp_uuid: str | None = None,
    detected_entries: tuple[BootEntry, ...] = tuple(),
    timeout_seconds: int = 5,
    default_entry: str = "fx11",
    use_theme: bool = True,
) -> str:
    if timeout_seconds < 0:
        raise BuilderError("FX Boot Manager timeout cannot be negative.")

    fx11 = BootEntry("FX11", WINDOWS_BOOT_PATH, fx11_esp_uuid, "fx11")
    lines = [
        "insmod part_gpt",
        "insmod fat",
        "insmod chain",
        "insmod search",
        "insmod search_fs_uuid",
        "insmod search_file",
        "insmod gfxterm",
        "insmod png",
        "set gfxmode=auto",
        "terminal_output gfxterm",
        f"set timeout={timeout_seconds}",
        f"set default='{_escape_grub(default_entry)}'",
    ]
    if use_theme:
        lines.extend(
            [
                "if [ -f ($root)/EFI/FX11/theme/theme.txt ]; then",
                "  set theme=($root)/EFI/FX11/theme/theme.txt",
                "  export theme",
                "fi",
            ]
        )

    def add_entry(entry: BootEntry, variable: str) -> None:
        identifier = entry.identifier or entry.title.lower().replace(" ", "-")
        lines.append("")
        lines.append(f"menuentry '{_escape_grub(entry.title)}' --id '{_escape_grub(identifier)}' {{")
        for command in _search_lines(entry, variable):
            lines.append(f"  {command}")
        lines.append(f"  chainloader (${variable}){_escape_grub(entry.efi_path)}")
        lines.append("}")

    add_entry(fx11, "fxesp")
    for index, entry in enumerate(detected_entries, start=1):
        if entry.efi_path.casefold() == WINDOWS_BOOT_PATH.casefold() and entry.fs_uuid == fx11_esp_uuid:
            continue
        add_entry(entry, f"os{index}")

    lines.extend(
        [
            "",
            "menuentry 'UEFI Firmware Settings' --id 'uefi-firmware' {",
            "  fwsetup",
            "}",
        ]
    )
    return "\n".join(lines) + "\n"


def default_theme() -> str:
    return "\n".join(
        [
            'title-text: "FX Boot Manager"',
            'title-font: "Unifont Regular 24"',
            'desktop-color: "#08131f"',
            'desktop-image: "background.png"',
            'message-color: "#ffffff"',
            'message-bg-color: "#08131f"',
            '+ boot_menu {',
            '  left = 18%',
            '  top = 30%',
            '  width = 64%',
            '  height = 45%',
            '  item_font = "Unifont Regular 18"',
            '  item_color = "#e8f7ff"',
            '  selected_item_color = "#ffffff"',
            '  selected_item_pixmap_style = "select_*.png"',
            '  item_height = 36',
            '  item_padding = 8',
            '}',
            '+ label {',
            '  left = 18%',
            '  top = 80%',
            '  text = "Your System. Your Rules."',
            '  color = "#d9f7ff"',
            '  font = "Unifont Regular 16"',
            '}',
            "",
        ]
    )


def build_unsigned_payload(
    destination: Path,
    *,
    fx11_esp_uuid: str | None = None,
    detected_entries: tuple[BootEntry, ...] = tuple(),
    timeout_seconds: int = 5,
    background: Path | None = None,
) -> BootManagerPayload:
    tool = shutil.which("grub-mkstandalone")
    if not tool:
        raise BuilderError(
            "grub-mkstandalone is required to build the current unsigned FX Boot Manager. "
            "On Debian/Mint install grub-efi-amd64-bin."
        )

    destination = destination.expanduser().resolve()
    efi_dir = destination / "EFI" / "FX11"
    theme_dir = efi_dir / "theme"
    work_dir = destination / ".fx11-grub-build"
    theme_dir.mkdir(parents=True, exist_ok=True)
    work_dir.mkdir(parents=True, exist_ok=True)

    config = efi_dir / "grub.cfg"
    config.write_text(
        grub_config(
            fx11_esp_uuid=fx11_esp_uuid,
            detected_entries=detected_entries,
            timeout_seconds=timeout_seconds,
        ),
        encoding="utf-8",
    )
    theme = theme_dir / "theme.txt"
    theme.write_text(default_theme(), encoding="utf-8")
    if background is not None:
        source = background.expanduser().resolve()
        if not source.is_file():
            raise BuilderError(f"FX Boot Manager background not found: {source}")
        shutil.copy2(source, theme_dir / "background.png")

    embedded_config = work_dir / "grub-standalone.cfg"
    embedded_config.write_text(
        "search --no-floppy --file --set=fxroot /EFI/FX11/grub.cfg\n"
        "configfile ($fxroot)/EFI/FX11/grub.cfg\n",
        encoding="utf-8",
    )
    efi = efi_dir / "fxbootx64.efi"
    proc = subprocess.run(
        [
            tool,
            "-O",
            "x86_64-efi",
            "-o",
            str(efi),
            f"boot/grub/grub.cfg={embedded_config}",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        message = proc.stderr.decode("utf-8", errors="replace").strip()
        raise BuilderError(f"grub-mkstandalone failed: {message or proc.returncode}")
    if not efi.is_file() or efi.stat().st_size == 0:
        raise BuilderError("FX Boot Manager EFI binary was not created.")

    shutil.rmtree(work_dir, ignore_errors=True)
    return BootManagerPayload(
        efi_binary=efi,
        grub_config=config,
        theme_config=theme,
        secure_boot_compatible=False,
    )
