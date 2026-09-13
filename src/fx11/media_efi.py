from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import math
import re
import shutil
import subprocess

from .iso import BuilderError, run_checked, sha256_file
from .media_theme import MediaThemePayload


MEDIA_EFI_ISO_PATH = "/FX11/media/efiboot.img"
MEDIA_GRUB_CONFIG_PATH = "/FX11/media/grub.cfg"
MEDIA_WINPE_READY_PATH = "/EFI/FX11/winpe-ready"
MEDIA_EFI_SIZE_SECTORS = 32768  # 16 MiB at 512 bytes/sector for the minimal image.
MEDIA_GRUB_MODULES = (
    "part_gpt",
    "fat",
    "iso9660",
    "search",
    "search_fs_file",
    "loopback",
    "chain",
    "video",
    "gfxterm",
    "gfxterm_background",
    "gfxmenu",
    "png",
    "font",
    "normal",
    "configfile",
)

_MIB = 1024 * 1024
_WINPE_RESERVE_MIB = 128
_WINPE_ROUND_MIB = 64


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


def _target_image_mib(
    *,
    windows_efi_image: Path | None,
    boot_wim: Path | None,
    boot_sdi: Path | None,
    theme: MediaThemePayload | None,
) -> int:
    if windows_efi_image is None and boot_wim is None and boot_sdi is None:
        return 16
    if windows_efi_image is None or boot_wim is None or boot_sdi is None:
        raise BuilderError(
            "FAT-resident WinPE media requires windows_efi_image, boot_wim and boot_sdi together."
        )

    required = windows_efi_image.stat().st_size + boot_wim.stat().st_size + boot_sdi.stat().st_size
    if theme is not None:
        required += sum(
            item.stat().st_size
            for item in (theme.theme_config, theme.background, theme.logo, theme.font)
        )
    required += _WINPE_RESERVE_MIB * _MIB
    mib = math.ceil(required / _MIB)
    return max(256, math.ceil(mib / _WINPE_ROUND_MIB) * _WINPE_ROUND_MIB)


def _mtools_exists(mdir: str, image: Path, target: str) -> bool:
    proc = subprocess.run(
        [mdir, "-i", str(image), target],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return proc.returncode == 0


def _ensure_mtools_dir(mdir: str, mmd: str, image: Path, target: str) -> None:
    if not _mtools_exists(mdir, image, target):
        run_checked([mmd, "-i", str(image), target])


def _copy_original_efi_tree(mcopy: str, source_image: Path, destination_image: Path, work: Path) -> None:
    extracted = work / "windows-efi"
    if extracted.exists():
        shutil.rmtree(extracted)
    extracted.mkdir(parents=True)

    proc = subprocess.run(
        [mcopy, "-s", "-i", str(source_image), "::*", str(extracted)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        detail = proc.stderr.decode("utf-8", errors="replace").strip()
        raise BuilderError(f"Unable to extract the original Microsoft EFI image: {detail or proc.returncode}")

    children = list(extracted.iterdir())
    if not children:
        raise BuilderError("The original Microsoft EFI image was unexpectedly empty.")
    for child in children:
        run_checked([mcopy, "-s", "-i", str(destination_image), "-o", str(child), "::/"])


def build_media_efi_payload(
    destination: Path,
    *,
    theme: MediaThemePayload | None = None,
    windows_efi_image: Path | None = None,
    boot_wim: Path | None = None,
    boot_sdi: Path | None = None,
) -> MediaEfiPayload:
    grub = _require_tool("grub-mkstandalone", "grub-efi-amd64-bin")
    mformat = _require_tool("mformat", "mtools")
    mmd = _require_tool("mmd", "mtools")
    mcopy = _require_tool("mcopy", "mtools")
    mdir = _require_tool("mdir", "mtools")

    destination = destination.expanduser().resolve()
    destination.mkdir(parents=True, exist_ok=True)
    work = destination / ".build"
    work.mkdir(parents=True, exist_ok=True)

    for path, label in (
        (windows_efi_image, "original Microsoft EFI image"),
        (boot_wim, "WinPE boot.wim"),
        (boot_sdi, "WinPE boot.sdi"),
    ):
        if path is not None and (not path.is_file() or path.stat().st_size == 0):
            raise BuilderError(f"{label} is missing or empty: {path}")

    embedded = work / "grub-standalone.cfg"
    embedded.write_text(embedded_media_config(), encoding="utf-8")

    efi = work / "BOOTX64.EFI"
    modules = " ".join(MEDIA_GRUB_MODULES)
    proc = subprocess.run(
        [
            grub,
            "-O",
            "x86_64-efi",
            "--modules",
            modules,
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

    target_mib = _target_image_mib(
        windows_efi_image=windows_efi_image,
        boot_wim=boot_wim,
        boot_sdi=boot_sdi,
        theme=theme,
    )
    sectors = target_mib * 2048
    format_cmd = [
        mformat,
        "-C",
        "-i",
        str(image),
        "-T",
        str(sectors),
        "-h",
        "64",
        "-s",
        "32",
        "-v",
        "FX11BOOT",
    ]
    if target_mib >= 64:
        format_cmd.append("-F")
    format_cmd.append("::")
    run_checked(format_cmd)

    if windows_efi_image is not None:
        _copy_original_efi_tree(mcopy, windows_efi_image, image, work)

    _ensure_mtools_dir(mdir, mmd, image, "::/EFI")
    _ensure_mtools_dir(mdir, mmd, image, "::/EFI/BOOT")
    run_checked([mcopy, "-i", str(image), "-o", str(efi), "::/EFI/BOOT/BOOTX64.EFI"])

    _ensure_mtools_dir(mdir, mmd, image, "::/EFI/FX11")
    if theme is not None:
        _ensure_mtools_dir(mdir, mmd, image, "::/EFI/FX11/theme")
        for source, target in (
            (theme.theme_config, "::/EFI/FX11/theme/theme.txt"),
            (theme.background, "::/EFI/FX11/theme/background.png"),
            (theme.logo, "::/EFI/FX11/theme/logo.png"),
            (theme.font, "::/EFI/FX11/theme/unicode.pf2"),
        ):
            run_checked([mcopy, "-i", str(image), "-o", str(source), target])

    if windows_efi_image is not None and boot_wim is not None and boot_sdi is not None:
        _ensure_mtools_dir(mdir, mmd, image, "::/sources")
        _ensure_mtools_dir(mdir, mmd, image, "::/boot")
        run_checked([mcopy, "-i", str(image), "-o", str(boot_wim), "::/sources/boot.wim"])
        run_checked([mcopy, "-i", str(image), "-o", str(boot_sdi), "::/boot/boot.sdi"])
        marker = work / "winpe-ready"
        marker.write_text("FX11 WinPE FAT payload\n", encoding="ascii")
        run_checked([mcopy, "-i", str(image), "-o", str(marker), f"::{MEDIA_WINPE_READY_PATH}"])

    if not image.is_file() or image.stat().st_size == 0:
        raise BuilderError("FX11 media EFI FAT image was not created.")

    return MediaEfiPayload(
        image=image,
        efi_binary=efi,
        embedded_config=embedded,
        sha256=sha256_file(image),
    )
