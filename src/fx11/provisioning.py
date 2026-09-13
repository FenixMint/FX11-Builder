from __future__ import annotations

from hashlib import sha256
from pathlib import Path

from .profiles import appx_targets


PRIVACY_SCRIPT = r'''
Write-Log "Applying privacy-balanced policy"

# Machine-wide policies. Required diagnostics remain enabled so servicing and security stay functional.
Set-RegDword "HKLM:\SOFTWARE\Policies\Microsoft\Windows\CloudContent" "DisableWindowsConsumerFeatures" 1
Set-RegDword "HKLM:\SOFTWARE\Policies\Microsoft\Windows\DataCollection" "AllowTelemetry" 1
Set-RegDword "HKLM:\SOFTWARE\Policies\Microsoft\Windows\AdvertisingInfo" "DisabledByGroupPolicy" 1
Set-RegDword "HKLM:\SOFTWARE\Policies\Microsoft\Windows\System" "EnableActivityFeed" 0
Set-RegDword "HKLM:\SOFTWARE\Policies\Microsoft\Windows\System" "PublishUserActivities" 0
Set-RegDword "HKLM:\SOFTWARE\Policies\Microsoft\Windows\System" "UploadUserActivities" 0
Set-RegDword "HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsAI" "DisableAIDataAnalysis" 1
Set-RegDword "HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsCopilot" "TurnOffWindowsCopilot" 1

# Seed privacy defaults for accounts created after Windows Setup.
$defaultHive = "$env:SystemDrive\Users\Default\NTUSER.DAT"
if (Test-Path $defaultHive) {
    & reg.exe load "HKU\FX11_Default" $defaultHive | Out-Null
    if ($LASTEXITCODE -eq 0) {
        $cdm = "Registry::HKEY_USERS\FX11_Default\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager"
        Set-RegDword $cdm "ContentDeliveryAllowed" 0
        Set-RegDword $cdm "OemPreInstalledAppsEnabled" 0
        Set-RegDword $cdm "PreInstalledAppsEnabled" 0
        Set-RegDword $cdm "PreInstalledAppsEverEnabled" 0
        Set-RegDword $cdm "SilentInstalledAppsEnabled" 0
        Set-RegDword $cdm "SoftLandingEnabled" 0
        Set-RegDword $cdm "SystemPaneSuggestionsEnabled" 0
        Set-RegDword $cdm "SubscribedContent-338388Enabled" 0
        Set-RegDword $cdm "SubscribedContent-338389Enabled" 0
        Set-RegDword $cdm "SubscribedContent-338393Enabled" 0
        Set-RegDword $cdm "SubscribedContent-353694Enabled" 0
        Set-RegDword $cdm "SubscribedContent-353696Enabled" 0
        Set-RegDword "Registry::HKEY_USERS\FX11_Default\Software\Microsoft\Windows\CurrentVersion\AdvertisingInfo" "Enabled" 0
        Set-RegDword "Registry::HKEY_USERS\FX11_Default\Software\Microsoft\Windows\CurrentVersion\Privacy" "TailoredExperiencesWithDiagnosticDataEnabled" 0
        Set-RegDword "Registry::HKEY_USERS\FX11_Default\Software\Policies\Microsoft\Windows\Explorer" "DisableSearchBoxSuggestions" 1
        & reg.exe unload "HKU\FX11_Default" | Out-Null
    } else {
        Write-Log "WARNING: could not load Default User registry hive"
    }
}
'''


def _ps_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def _sha256_bytes(data: bytes) -> str:
    return sha256(data).hexdigest()


def powershell_script(profile_ids: list[str]) -> str:
    targets = appx_targets(profile_ids)
    target_lines = ",\n    ".join(_ps_quote(item) for item in targets)
    tiny_enabled = "tiny11-safe" in profile_ids
    privacy_enabled = "privacy-balanced" in profile_ids

    parts = [r'''$ErrorActionPreference = "Continue"
$ProgressPreference = "SilentlyContinue"
$logDir = Join-Path $env:ProgramData "FX11"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$logFile = Join-Path $logDir "provisioning.log"

function Write-Log([string]$Message) {
    $line = "[{0}] {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $Message
    Add-Content -Path $logFile -Value $line -Encoding UTF8
    Write-Output $line
}

function Set-RegDword([string]$Path, [string]$Name, [int]$Value) {
    try {
        New-Item -Path $Path -Force | Out-Null
        New-ItemProperty -Path $Path -Name $Name -PropertyType DWord -Value $Value -Force | Out-Null
        Write-Log "Registry: $Path / $Name = $Value"
    } catch {
        Write-Log "WARNING registry failure: $Path / $Name : $($_.Exception.Message)"
    }
}

Write-Log "FX11 Builder provisioning started"
''']

    if tiny_enabled:
        parts.append(f'''$AppxTargets = @(
    {target_lines}
)

Write-Log "Applying tiny11-safe application profile"
$provisioned = @(Get-AppxProvisionedPackage -Online -ErrorAction SilentlyContinue)
foreach ($target in $AppxTargets) {{
    foreach ($pkg in @($provisioned | Where-Object {{ $_.DisplayName -eq $target -or $_.PackageName -like "$target*" }})) {{
        try {{
            Write-Log "Deprovisioning $($pkg.PackageName)"
            Remove-AppxProvisionedPackage -Online -PackageName $pkg.PackageName -AllUsers -ErrorAction Stop | Out-Null
        }} catch {{
            Write-Log "WARNING deprovision failed: $($pkg.PackageName) : $($_.Exception.Message)"
        }}
    }}
}}

# SetupComplete normally runs before normal user accounts exist, but remove matching packages
# from any accounts already present (custom/OEM media can create them earlier).
$installed = @(Get-AppxPackage -AllUsers -ErrorAction SilentlyContinue)
foreach ($target in $AppxTargets) {{
    foreach ($pkg in @($installed | Where-Object {{ $_.Name -eq $target -or $_.PackageFullName -like "$target*" }})) {{
        if ($pkg.NonRemovable) {{
            Write-Log "Keeping non-removable package $($pkg.PackageFullName)"
            continue
        }}
        try {{
            Write-Log "Removing installed package $($pkg.PackageFullName)"
            Remove-AppxPackage -Package $pkg.PackageFullName -AllUsers -ErrorAction Stop
        }} catch {{
            Write-Log "WARNING installed package removal failed: $($pkg.PackageFullName) : $($_.Exception.Message)"
        }}
    }}
}}
''')

    if privacy_enabled:
        parts.append(PRIVACY_SCRIPT)

    parts.append(r'''
Write-Log "FX11 Builder provisioning completed"
exit 0
''')
    return "\n".join(parts)


def setup_complete_script(expected_ps1_sha256: str) -> str:
    return rf'''@echo off
setlocal
set "LOGDIR=%ProgramData%\FX11"
if not exist "%LOGDIR%" mkdir "%LOGDIR%"
set "FX11PS=%WINDIR%\Setup\Scripts\FX11.ps1"
set "EXPECTED={expected_ps1_sha256.lower()}"
echo [%DATE% %TIME%] FX11 Builder SetupComplete starting>>"%LOGDIR%\setupcomplete.log"
for /f "usebackq delims=" %%H in (`powershell.exe -NoLogo -NoProfile -NonInteractive -Command "(Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $env:WINDIR 'Setup\Scripts\FX11.ps1')).Hash.ToLowerInvariant()"`) do set "ACTUAL=%%H"
if /I not "%ACTUAL%"=="%EXPECTED%" (
  echo [%DATE% %TIME%] SECURITY ERROR: FX11.ps1 SHA256 mismatch. Expected %EXPECTED%, got %ACTUAL%>>"%LOGDIR%\setupcomplete.log"
  exit /b 10
)
echo [%DATE% %TIME%] FX11.ps1 integrity verified: %ACTUAL%>>"%LOGDIR%\setupcomplete.log"
powershell.exe -NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "%FX11PS%" >>"%LOGDIR%\setupcomplete.log" 2>&1
set "RC=%ERRORLEVEL%"
echo [%DATE% %TIME%] FX11 PowerShell exit code %RC%>>"%LOGDIR%\setupcomplete.log"
exit /b %RC%
'''


def write_provisioning_files(root: Path, profile_ids: list[str]) -> tuple[Path, Path, dict[str, str]]:
    scripts = root / "scripts"
    scripts.mkdir(parents=True, exist_ok=True)
    setup = scripts / "SetupComplete.cmd"
    ps1 = scripts / "FX11.ps1"

    ps1_text = powershell_script(profile_ids)
    ps1.write_text(ps1_text, encoding="utf-8-sig", newline="\r\n")
    ps1_hash = _sha256_bytes(ps1.read_bytes())

    setup.write_text(setup_complete_script(ps1_hash), encoding="utf-8", newline="\r\n")
    hashes = {
        "SetupComplete.cmd": _sha256_bytes(setup.read_bytes()),
        "FX11.ps1": ps1_hash,
    }
    return setup, ps1, hashes
