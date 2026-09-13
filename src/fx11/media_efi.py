from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import shutil
import subprocess

from .iso import BuilderError, run_checked, sha256_file


MEDIA_EFI_ISO_PATH = "/FX11/media/efiboot.img"
MEDIA_GRUB_CONFIG_PATH = "/FX11/media/grub.cfg"
MEDIA_EFI_SIZE_SECTORS = 32768  # 16 MiB at 512 bytes/sector


@dataclass(frozen=True)
class MediaEfiPayload:
    image: Path
    efi_binary: Path
    embedded_config: Path
    sha256: str


def embedded_media_config() -> str:
    return (
        f"search --no-floppy --file --set=fxmedia {MEDIA_GRUB_CONFIG_PATH}\n"
        f"configfile ($fxmedia){MEDIA_GRUB_CONFIG_PATH}\n"
    )


def parse_efi_el_torito_path(report: str) -> str:
    """Return the file-backed EFI El Torito image path from xorriso command report."""
    pattern = re.compile(r"efi_path=(?:'([^']+)'|\"([^\"]+)\"|(\S+))")
    for line in report.splitlines():
        if "efi_path=" not in line:
            continue
        match = pattern.search(line)
        if not match:
            continue
        value = next((item for item in match.groups() if item is not None), "")
        if value.startswith("/"):
            return value
        if value.startswith("--interval:"):
            raise BuilderError(
                "Source ISO uses an interval/appended-partition EFI boot image. "
                "FX11 GParted mainline currently requires a file-backed EFI El Torito image."
            )
    raise BuilderError("Unable to discover a file-backed EFI El Torito image in the source ISO.")


def discover_efi_el_torito_path(source_iso: Path) -> str:
    proc = run_checked(
        ["xorriso", "-indev", str(source_iso), "-report_el_torito", "cmd"],
        capture_output=True,
    )
    report = (proc.stdout + proc.stderr).decode("utf-8", errors="replace")
    return parse_efi_el_torito_path(report)


def _require_tool(command: str, package_hint: str) -> str:
    tool = shutil.which(command)
    if not tool:
        raise BuilderError(
            f"{command} is required to build the FX11 installation-media UEFI image. "
            f"Install {package_hint}."
        )
    return tool


def build_media_efi_payload(destination: Path) -> MediaEfiPayload:
    grub = _require_tool("grub-mkstandalone", "grub-efi-amd64-bin")
    mformat = _require_tool("mformat", "mtools")
    mmd = _require_tool("mmd", "mtools")
    mcopy = _require_tool("mcopy", "mtools")

    destination = destination.expanduser().resolve()
    destination.mkdir(parents=True, exist_ok=True)
    work = destination / ".build"
    work.mkdir(parents=True, exist_ok=True)

    embedded = work / "grub-standalone.cfg"
    embedded.write_text(embedded_media_config(), encoding="utf-8")

    efi = work / "BOOTX64.EFI"
    proc = subprocess.run(
        [
            grub,
            "-O",
            "x86_64-efi",
            "-o",
            str(efi),
            f"boot/grub/grub.cfg={embedded}",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        detail = proc.stderr.decode("utf-8", errors="replace").strip()
        raise BuilderError(f"grub-mkstandalone failed for FX11 media boot: {detail or proc.returncode}")
    if not efi.is_file() or efi.stat().st_size == 0:
        raise BuilderError("FX11 media BOOTX64.EFI was not created.")

    image = destination / "efiboot.img"
    image.unlink(missing_ok=True)

    # mformat -C creates the image file and a minimal FAT filesystem. 16 MiB
    # stays comfortably below xorriso's normal EFI El Torito image limit.
    run_checked([
        mformat,
        "-C",
        "-i",
        str(image),
        "-T",
        str(MEDIA_EFI_SIZE_SECTORS),
        "-h",
        "64",
        "-s",
        "32",
        "-v",
        "FX11BOOT",
        "::",
    ])
    run_checked([mmd, "-i", str(image), "::/EFI"])
    run_checked([mmd, "-i", str(image), "::/EFI/BOOT"])
    run_checked([mcopy, "-i", str(image), "-o", str(efi), "::/EFI/BOOT/BOOTX64.EFI"])

    if not image.is_file() or image.stat().st_size == 0:
        raise BuilderError("FX11 media EFI FAT image was not created.")

    return MediaEfiPayload(
        image=image,
        efi_binary=efi,
        embedded_config=embedded,
        sha256=sha256_file(image),
    )
