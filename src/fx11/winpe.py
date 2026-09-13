from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class WinPEPayload:
    startnet: Path
    launcher: Path
    readme: Path


STARTNET = r'''@echo off
wpeinit
call X:\FX11\fx11-launch.cmd
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

This payload is injected into boot.wim image index 2 when available (Windows Setup/WinPE image), otherwise index 1.
It replaces Startnet.cmd so WinPE initializes devices/networking with wpeinit and then starts the FX11 launcher.

The current launcher is deliberately non-destructive. It proves that FX11 owns the boot-to-installer handoff before the graphical FX Partition Manager is added.
'''


def write_winpe_payload(root: Path) -> WinPEPayload:
    root.mkdir(parents=True, exist_ok=True)
    startnet = root / "startnet.cmd"
    launcher = root / "fx11-launch.cmd"
    readme = root / "README.txt"
    startnet.write_text(STARTNET.replace("\n", "\r\n"), encoding="ascii")
    launcher.write_text(LAUNCHER.replace("\n", "\r\n"), encoding="ascii")
    readme.write_text(README, encoding="utf-8")
    return WinPEPayload(startnet=startnet, launcher=launcher, readme=readme)
