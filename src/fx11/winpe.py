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
    partition_manager: Path
    installer: Path
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
setlocal EnableExtensions
:menu
cls
echo ================================================================
echo                         FX11 Installer
echo ================================================================
echo.
echo FX11 installation environment is ready.
echo Current development media requires Secure Boot OFF when using
 echo the unsigned FX Boot Manager.
echo.
echo [1] Start FX Partition Manager
echo [2] Open command prompt
echo [3] Start stock Windows Setup fallback
echo [R] Reboot
echo.
choice /c 123R /n /m "Select > "
if errorlevel 4 wpeutil reboot
if errorlevel 3 goto setup
if errorlevel 2 cmd.exe
if errorlevel 1 call X:\FX11\fx11-partition.cmd
goto menu

:setup
if exist X:\sources\setup.exe X:\sources\setup.exe
if exist X:\setup.exe X:\setup.exe
for %%D in (C D E F G H I J K L M N O P Q R S T U V W Y Z) do if exist %%D:\setup.exe %%D:\setup.exe
echo Windows Setup fallback was not found.
pause
goto menu
'''

PARTITION_MANAGER = r'''@echo off
setlocal EnableExtensions EnableDelayedExpansion

:menu
cls
echo ================================================================
echo                    FX Partition Manager
echo ================================================================
echo.
echo Current development interface: text mode.
echo Partition changes are applied only after explicit confirmation.
echo.
echo [1] FX11 only              - ERASE selected disk
echo [2] FX11 + Other OS        - ERASE selected disk, leave free space
echo [3] Custom / manual        - use DiskPart yourself
echo [B] Back
echo.
choice /c 123B /n /m "Select layout > "
if errorlevel 4 exit /b 0
if errorlevel 3 goto custom
if errorlevel 2 goto other
if errorlevel 1 goto only
goto menu

:list_disks
> X:\FX11\list-disks.txt echo list disk
diskpart /s X:\FX11\list-disks.txt
exit /b 0

:check_letters
if exist S:\ goto letters_busy
if exist W:\ goto letters_busy
if exist R:\ goto letters_busy
exit /b 0

:letters_busy
echo.
echo ERROR: One of the temporary installer letters S:, W: or R: is already in use.
echo Disconnect unnecessary storage or change its drive letter before continuing.
pause
exit /b 2

:select_disk
call :list_disks
echo.
set "DISK="
set /p "DISK=Physical disk number to use > "
echo(!DISK!| findstr /r "^[0-9][0-9]*$" >nul || goto bad_disk
exit /b 0

:bad_disk
echo Invalid disk number.
pause
exit /b 2

:confirm_erase
echo.
echo WARNING: ALL partitions and data on physical disk !DISK! will be erased.
echo FX11 will not modify any other disk in this guided operation.
choice /c YN /n /m "Erase disk !DISK! and continue? [Y/N] > "
if errorlevel 2 exit /b 2
exit /b 0

:only
call :check_letters || goto menu
call :select_disk || goto menu
call :confirm_erase || goto menu
set "SCRIPT=X:\FX11\guided-diskpart.txt"
> "!SCRIPT!" echo select disk !DISK!
>>"!SCRIPT!" echo clean
>>"!SCRIPT!" echo convert gpt
>>"!SCRIPT!" echo create partition efi size=300
>>"!SCRIPT!" echo format quick fs=fat32 label="System"
>>"!SCRIPT!" echo assign letter=S
>>"!SCRIPT!" echo create partition msr size=16
>>"!SCRIPT!" echo create partition primary
>>"!SCRIPT!" echo format quick fs=ntfs label="FX11"
>>"!SCRIPT!" echo assign letter=W
>>"!SCRIPT!" echo select volume W
>>"!SCRIPT!" echo shrink desired=1024 minimum=1024
>>"!SCRIPT!" echo create partition primary
>>"!SCRIPT!" echo format quick fs=ntfs label="Recovery"
>>"!SCRIPT!" echo assign letter=R
>>"!SCRIPT!" echo set id=de94bba4-06d1-4d40-a16a-bfd50179d6ac
>>"!SCRIPT!" echo gpt attributes=0x8000000000000001
goto apply_guided

:other
call :check_letters || goto menu
call :select_disk || goto menu
set "FXGB="
echo.
echo Enter the FX11 partition size in GiB.
echo Minimum guided size: 64 GiB. Remaining space stays unallocated for Other OS.
set /p "FXGB=FX11 size in GiB > "
echo(!FXGB!| findstr /r "^[0-9][0-9]*$" >nul || goto bad_size
set /a FXMIB=FXGB*1024
if !FXMIB! LSS 65536 goto bad_size
call :confirm_erase || goto menu
set "SCRIPT=X:\FX11\guided-diskpart.txt"
> "!SCRIPT!" echo select disk !DISK!
>>"!SCRIPT!" echo clean
>>"!SCRIPT!" echo convert gpt
>>"!SCRIPT!" echo create partition efi size=300
>>"!SCRIPT!" echo format quick fs=fat32 label="System"
>>"!SCRIPT!" echo assign letter=S
>>"!SCRIPT!" echo create partition msr size=16
>>"!SCRIPT!" echo create partition primary size=!FXMIB!
>>"!SCRIPT!" echo format quick fs=ntfs label="FX11"
>>"!SCRIPT!" echo assign letter=W
>>"!SCRIPT!" echo create partition primary size=1024
>>"!SCRIPT!" echo format quick fs=ntfs label="Recovery"
>>"!SCRIPT!" echo assign letter=R
>>"!SCRIPT!" echo set id=de94bba4-06d1-4d40-a16a-bfd50179d6ac
>>"!SCRIPT!" echo gpt attributes=0x8000000000000001
goto apply_guided

:bad_size
echo Invalid size. Enter a whole number of GiB, at least 64.
pause
goto menu

:apply_guided
cls
echo Applying partition layout to disk !DISK! ...
diskpart /s "!SCRIPT!"
if not exist S:\ goto partition_failed
if not exist W:\ goto partition_failed
if not exist R:\ goto partition_failed
echo.
echo Partition layout created successfully.
echo EFI System : S:
echo FX11 target: W:
echo Recovery   : R:
echo.
choice /c YN /n /m "Continue directly to FX11 installation? [Y/N] > "
if errorlevel 2 goto menu
call X:\FX11\fx11-install.cmd
exit /b %errorlevel%

:partition_failed
echo.
echo ERROR: Expected FX11 partition layout was not created.
echo Installation will NOT start. Review DiskPart output above.
pause
goto menu

:custom
cls
echo ================================================================
echo                 FX Partition Manager - Custom
echo ================================================================
echo.
echo Custom mode currently uses DiskPart directly.
echo Before continuing to FX11 Installer assign:
echo   S: to the FAT32 EFI System Partition
echo   W: to the NTFS FX11 / Windows target
echo   R: to Recovery if you want WinRE configured now
echo.
echo No automatic clean/format is performed in Custom mode.
echo Type EXIT in DiskPart when finished.
echo.
pause
diskpart
if not exist S:\ goto custom_missing
if not exist W:\ goto custom_missing
echo.
choice /c YN /n /m "Use S: as EFI and W: as the FX11 target and continue? [Y/N] > "
if errorlevel 2 goto menu
call X:\FX11\fx11-install.cmd
exit /b %errorlevel%

:custom_missing
echo.
echo S: and W: were not both found. Nothing will be installed.
pause
goto menu
'''

INSTALLER = r'''@echo off
setlocal EnableExtensions
cls
echo ================================================================
echo                         FX11 Installer
echo ================================================================
echo.

if not exist W:\ goto missing_target
if not exist S:\ goto missing_esp

set "MEDIA="
for %%D in (C D E F G H I J K L M N O P Q R S T U V W Y Z) do (
  if exist %%D:\FX11-manifest.json if exist %%D:\sources\install.wim set "MEDIA=%%D:"
)
if not defined MEDIA goto no_media

echo Installation media: %MEDIA%
echo Windows target   : W:
echo EFI System       : S:
if exist R:\ echo Recovery         : R:
echo.
echo The FX11 ISO contains one selected Windows edition at image index 1.
choice /c YN /n /m "Apply the FX11 image to W: now? [Y/N] > "
if errorlevel 2 exit /b 2

echo.
echo [1/5] Applying Windows image...
dism /Apply-Image /ImageFile:"%MEDIA%\sources\install.wim" /Index:1 /ApplyDir:W:\
if errorlevel 1 goto install_failed

echo.
echo [2/5] Staging FX11 provisioning and manifest...
if not exist W:\Windows\Setup\Scripts mkdir W:\Windows\Setup\Scripts
copy /y "%MEDIA%\sources\$OEM$\$$\Setup\Scripts\SetupComplete.cmd" W:\Windows\Setup\Scripts\SetupComplete.cmd >nul
if errorlevel 1 goto install_failed
copy /y "%MEDIA%\sources\$OEM$\$$\Setup\Scripts\FX11.ps1" W:\Windows\Setup\Scripts\FX11.ps1 >nul
if errorlevel 1 goto install_failed
if not exist W:\FX11 mkdir W:\FX11
copy /y "%MEDIA%\FX11-manifest.json" W:\FX11\manifest.json >nul
if errorlevel 1 goto install_failed

echo.
echo [3/5] Creating standard Windows UEFI boot files...
bcdboot W:\Windows /s S: /f UEFI
if errorlevel 1 goto install_failed

echo.
echo [4/5] Staging FX Boot Manager on the EFI System Partition...
if exist "%MEDIA%\FX11\boot\EFI\FX11\fxbootx64.efi" (
  if not exist S:\EFI\FX11 mkdir S:\EFI\FX11
  xcopy "%MEDIA%\FX11\boot\EFI\FX11\*" S:\EFI\FX11\ /E /I /H /Y >nul
  if errorlevel 1 goto install_failed
) else (
  echo WARNING: FX Boot Manager payload was not found on the installation media.
)

echo.
echo [5/5] Configuring Windows Recovery when R: is available...
if exist R:\ (
  if exist W:\Windows\System32\Recovery\Winre.wim (
    if not exist R:\Recovery\WindowsRE mkdir R:\Recovery\WindowsRE
    copy /y W:\Windows\System32\Recovery\Winre.wim R:\Recovery\WindowsRE\Winre.wim >nul
    reagentc /setreimage /path R:\Recovery\WindowsRE /target W:\Windows
    if errorlevel 1 echo WARNING: WinRE image path could not be registered automatically.
    reagentc /enable /target W:\Windows
    if errorlevel 1 echo WARNING: WinRE could not be enabled automatically.
  ) else (
    echo WARNING: Winre.wim was not found in the applied image.
  )
) else (
  echo Recovery partition R: is not present; continuing without WinRE configuration.
)

echo.
echo ================================================================
echo FX11 image deployment completed.
echo ================================================================
echo.
echo Windows Boot Manager is configured and the FX Boot Manager files
 echo are staged on the ESP. Automatic firmware-default activation of
 echo FX Boot Manager is NOT enabled in this development build yet.
echo.
echo Remove the installation media when the machine restarts.
choice /c RN /n /m "[R] Reboot now  [N] Return to manager > "
if errorlevel 2 exit /b 0
wpeutil reboot
exit /b 0

:missing_target
echo ERROR: FX11 target W: is missing. Installation has not started.
pause
exit /b 2

:missing_esp
echo ERROR: EFI System Partition S: is missing. Installation has not started.
pause
exit /b 2

:no_media
echo ERROR: Could not find FX11 installation media containing sources\install.wim.
pause
exit /b 2

:install_failed
echo.
echo ERROR: FX11 installation failed. The computer will not be rebooted automatically.
echo Review the command output above before making any further disk changes.
pause
exit /b 2
'''

README = '''FX11 WinPE bootstrap

This payload is injected into the bootable image contained in sources/boot.wim.
The builder reads the WIM boot index and uses it when available; if no boot index
is declared it falls back to Windows Setup image 2 when present, otherwise image 1.

Winpeshl.ini launches Startnet.cmd explicitly. Startnet.cmd runs wpeinit first and
then hands control to the FX11 launcher. This avoids depending on stock Windows
Setup being the WinPE shell.

Development end-to-end path:

  WinPE -> FX Partition Manager (text mode) -> FX11 Installer
        -> DISM /Apply-Image -> BCDBoot -> optional WinRE -> reboot/OOBE

Guided partitioning requires explicit destructive confirmation and modifies only
the physical disk number entered by the user. Custom mode does not automatically
clean or format a disk; the user assigns S: to ESP and W: to the FX11 target.

The installer stages the unsigned development FX Boot Manager files on the ESP,
but this milestone does not yet make FX Boot Manager the firmware-default NVRAM
entry automatically. Windows Boot Manager remains the reliable boot path for the
first real-hardware installation test.
'''


def _crlf(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\n", "\r\n")


def write_winpe_payload(root: Path) -> WinPEPayload:
    root.mkdir(parents=True, exist_ok=True)
    startnet = root / "startnet.cmd"
    winpeshl = root / "winpeshl.ini"
    launcher = root / "fx11-launch.cmd"
    partition_manager = root / "fx11-partition.cmd"
    installer = root / "fx11-install.cmd"
    readme = root / "README.txt"
    startnet.write_text(_crlf(STARTNET), encoding="ascii")
    winpeshl.write_text(_crlf(WINPESHL), encoding="ascii")
    launcher.write_text(_crlf(LAUNCHER), encoding="ascii")
    partition_manager.write_text(_crlf(PARTITION_MANAGER), encoding="ascii")
    installer.write_text(_crlf(INSTALLER), encoding="ascii")
    readme.write_text(README, encoding="utf-8")
    return WinPEPayload(
        startnet=startnet,
        winpeshl=winpeshl,
        launcher=launcher,
        partition_manager=partition_manager,
        installer=installer,
        readme=readme,
    )


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
            f"add {_quote_update_path(payload.partition_manager)} /FX11/fx11-partition.cmd",
            f"add {_quote_update_path(payload.installer)} /FX11/fx11-install.cmd",
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
