from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

from .iso import BuilderError, run_checked, sha256_file


@dataclass(frozen=True)
class WinPEPayload:
    startnet: Path
    winpeshl: Path
    launcher: Path
    readme: Path


@dataclass(frozen=True)
class CustomizedBootWim:
    path: Path
    image_index: int
    source_sha256: str
    output_sha256: str
    payload: WinPEPayload


STARTNET = r'''@echo off
wpeinit
call X:\FX11\fx11-launch.cmd
'''

WINPESHL = r'''[LaunchApps]
%SYSTEMROOT%\System32\cmd.exe, /c %SYSTEMROOT%\System32\startnet.cmd
'''

LAUNCHER = r'''@echo off
setlocal
cls
echo ================================================================
echo                         FX11 Installer
echo ================================================================
echo.
echo FX Partition Manager bootstrap loaded.
echo.
echo Current development media intentionally requires Secure Boot OFF
echo when the unsigned FX Boot Manager is selected.
echo.
echo The production GUI will replace this bootstrap shell.
echo.
echo [1] Open DiskPart for manual inspection only
echo [2] Open command prompt
echo [3] Start stock Windows Setup fallback
echo [R] Reboot
echo.
choice /c 123R /n /m "Select > "
if errorlevel 4 wpeutil reboot
if errorlevel 3 goto setup
if errorlevel 2 cmd.exe
if errorlevel 1 diskpart.exe
goto :eof

:setup
if exist X:\sources\setup.exe X:\sources\setup.exe
if exist X:\setup.exe X:\setup.exe
if exist D:\setup.exe D:\setup.exe
if exist E:\setup.exe E:\setup.exe
echo Windows Setup fallback was not found.
pause
'''

README = '''FX11 WinPE bootstrap

This payload is injected into the bootable image contained in sources/boot.wim.
The builder reads the WIM boot index and uses it when available; if no boot index
is declared it falls back to Windows Setup image 2 when present, otherwise image 1.

Winpeshl.ini launches Startnet.cmd explicitly. Startnet.cmd runs wpeinit first and
then hands control to the FX11 launcher. This avoids depending on stock Windows
Setup being the WinPE shell.

The current launcher is deliberately non-destructive. It proves that FX11 owns
the boot-to-installer handoff before the graphical FX Partition Manager is added.
'''


def _crlf(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\n", "\r\n")


def write_winpe_payload(root: Path) -> WinPEPayload:
    root.mkdir(parents=True, exist_ok=True)
    startnet = root / "startnet.cmd"
    winpeshl = root / "winpeshl.ini"
    launcher = root / "fx11-launch.cmd"
    readme = root / "README.txt"
    startnet.write_text(_crlf(STARTNET), encoding="ascii")
    winpeshl.write_text(_crlf(WINPESHL), encoding="ascii")
    launcher.write_text(_crlf(LAUNCHER), encoding="ascii")
    readme.write_text(README, encoding="utf-8")
    return WinPEPayload(startnet=startnet, winpeshl=winpeshl, launcher=launcher, readme=readme)


def select_boot_image_index(xml_text: str) -> int:
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        raise BuilderError(f"Unable to parse boot.wim metadata: {exc}") from exc

    indexes: list[int] = []
    for image in root.findall("IMAGE"):
        try:
            indexes.append(int(image.attrib.get("INDEX", "0")))
        except ValueError:
            continue
    indexes = sorted(index for index in indexes if index > 0)
    if not indexes:
        raise BuilderError("boot.wim contains no usable image indexes.")

    boot = root.find("BOOT")
    if boot is not None:
        candidates = [boot.attrib.get("INDEX"), (boot.text or "").strip()]
        for value in candidates:
            if not value:
                continue
            try:
                boot_index = int(value)
            except ValueError:
                continue
            if boot_index in indexes:
                return boot_index

    if 2 in indexes:
        return 2
    return indexes[0]


def _read_boot_image_index(boot_wim: Path) -> int:
    proc = run_checked(["wimlib-imagex", "info", str(boot_wim), "--xml"], capture_output=True)
    raw = proc.stdout
    try:
        text = raw.decode("utf-16")
    except UnicodeError:
        text = raw.decode("utf-8", errors="replace")
    return select_boot_image_index(text)


def _extract_boot_wim(source_iso: Path, destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        [
            "xorriso",
            "-osirrox", "on",
            "-indev", str(source_iso),
            "-extract", "/sources/boot.wim", str(destination),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0 or not destination.is_file() or destination.stat().st_size == 0:
        detail = (proc.stderr or proc.stdout or b"").decode("utf-8", errors="replace").strip()
        raise BuilderError(f"Unable to extract /sources/boot.wim from source ISO.\n{detail}")
    return destination


def _quote_update_path(path: Path) -> str:
    value = str(path.resolve())
    if '"' in value:
        raise BuilderError("WinPE payload path contains an unsupported quote character.")
    return f'"{value}"'


def winpe_update_commands(payload: WinPEPayload) -> str:
    return "\n".join(
        [
            f"add {_quote_update_path(payload.startnet)} /Windows/System32/startnet.cmd",
            f"add {_quote_update_path(payload.winpeshl)} /Windows/System32/winpeshl.ini",
            f"add {_quote_update_path(payload.launcher)} /FX11/fx11-launch.cmd",
            f"add {_quote_update_path(payload.readme)} /FX11/README.txt",
        ]
    ) + "\n"


def customize_boot_wim(source_iso: Path, work_root: Path) -> CustomizedBootWim:
    source_iso = source_iso.expanduser().resolve()
    if not source_iso.is_file():
        raise BuilderError(f"Source ISO not found: {source_iso}")

    work_root.mkdir(parents=True, exist_ok=True)
    boot_wim = _extract_boot_wim(source_iso, work_root / "boot.wim")
    source_hash = sha256_file(boot_wim)
    image_index = _read_boot_image_index(boot_wim)
    payload = write_winpe_payload(work_root / "payload")
    commands = winpe_update_commands(payload)

    proc = subprocess.run(
        [
            "wimlib-imagex",
            "update",
            str(boot_wim),
            str(image_index),
            "--check",
            "--rebuild",
        ],
        input=commands.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or b"").decode("utf-8", errors="replace").strip()
        raise BuilderError(f"Unable to inject FX11 startup into boot.wim image {image_index}.\n{detail}")

    run_checked(["wimlib-imagex", "verify", str(boot_wim)])
    output_hash = sha256_file(boot_wim)
    if output_hash == source_hash:
        raise BuilderError("boot.wim hash did not change after FX11 WinPE customization.")

    return CustomizedBootWim(
        path=boot_wim,
        image_index=image_index,
        source_sha256=source_hash,
        output_sha256=output_hash,
        payload=payload,
    )
