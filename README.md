# OS11vLIN

OS11vLIN is a Linux-native Windows 11 ISO builder inspired by the **tiny11maker** approach, but designed around a conservative and serviceable V1 profile.

It runs on Linux Mint, LMDE and Debian, keeps the original ISO untouched, lets you choose the exact Windows image contained in the ISO (Home, Pro, Pro N, Education, Enterprise, etc.), exports only that image into the new ISO, and applies `tiny11-safe + privacy-balanced` automatically during Windows Setup.

## What V1 does

- checks the Linux build host,
- reads Microsoft Windows 11 ISO files directly,
- supports both `sources/install.wim` and `sources/install.esd`,
- lists every Windows edition/index present in the source image,
- lets you select an edition interactively or with CLI flags,
- exports the selected image with `wimlib` into a single-image `install.wim`,
- injects Windows `SetupComplete` provisioning,
- removes a conservative list of consumer AppX packages with native Windows servicing cmdlets,
- applies a balanced privacy policy,
- keeps Defender, Windows Update, Microsoft Store, SmartScreen, Edge/WebView2, Terminal and WinRE,
- preserves the source ISO boot structure through xorriso boot replay,
- validates the generated ISO,
- writes a build manifest and SHA-256 checksum,
- can boot the result in QEMU with UEFI/OVMF for testing.

## Why application removal happens during SetupComplete

`wimlib` is excellent for reading, exporting and modifying WIM file contents, but it is not a full replacement for Windows DISM servicing. OS11vLIN therefore does not blindly delete Windows component directories from a WIM.

Instead, the Linux builder prepares the image and injects a `SetupComplete` script. During Windows installation, Windows itself uses `Remove-AppxProvisionedPackage` and `Remove-AppxPackage` to remove declared applications. This keeps servicing much safer than direct filesystem deletion.

## Installation on Mint / LMDE / Debian

Clone the repository and run:

```bash
git clone https://github.com/FenixMint/OS11vLIN.git
cd OS11vLIN
chmod +x scripts/bootstrap-debian.sh
./scripts/bootstrap-debian.sh
. .venv/bin/activate
```

The bootstrap installs:

- Python 3 + venv,
- `wimtools` / `wimlib-imagex`,
- `xorriso`,
- QEMU,
- OVMF firmware.

Then verify the host:

```bash
os11vlin doctor
```

The ISO builder itself requires only `wimlib-imagex` and `xorriso`. QEMU/OVMF are optional and used for VM testing.

## 1. Inspect the source ISO

```bash
os11vlin inspect ~/ISO/Win11.iso
```

Example:

```text
Source : /home/user/ISO/Win11.iso
SHA256 : ...
Image  : ESD

Available Windows images:
   1. Windows 11 Home [Core]
   2. Windows 11 Home N [CoreN]
   6. Windows 11 Pro [Professional]
   7. Windows 11 Pro N [ProfessionalN]
  10. Windows 11 Education [Education]
```

The list is read from the actual `install.wim`/`install.esd`. OS11vLIN does not assume fixed image indexes.

## 2. Build interactively

```bash
os11vlin build ~/ISO/Win11.iso
```

OS11vLIN displays the images and asks:

```text
Select Windows image index >
```

Choose Home, Pro or any other edition contained in the ISO.

The default profiles are:

```text
tiny11-safe
privacy-balanced
```

## 3. Build non-interactively

By index:

```bash
os11vlin build ~/ISO/Win11.iso --index 6 -o ~/ISO/Win11-Pro-OS11vLIN.iso
```

By full edition name:

```bash
os11vlin build ~/ISO/Win11.iso --edition "Windows 11 Pro"
```

By WIM EditionID:

```bash
os11vlin build ~/ISO/Win11.iso --edition Professional
```

Use `--force` only when intentionally replacing an existing output ISO. OS11vLIN always refuses to overwrite the source ISO.

## Dry run

```bash
os11vlin build ~/ISO/Win11.iso --edition "Windows 11 Pro" --dry-run
```

This inspects the source, resolves the selected edition and prints all profile actions without creating an ISO.

You can also inspect the profiles alone:

```bash
os11vlin plan
os11vlin profiles
```

## tiny11-safe profile

The profile removes selected consumer applications such as:

- Clipchamp,
- News and Weather,
- Get Help / Get Started,
- People,
- Solitaire,
- Feedback Hub,
- Maps,
- Phone Link,
- consumer Xbox packages,
- Movies & TV / legacy media package,
- consumer Teams,
- Family,
- Quick Assist.

V1 intentionally preserves the serviceability-critical and commonly required components:

- Microsoft Store,
- Windows Update,
- Microsoft Defender,
- SmartScreen,
- Edge and WebView2,
- Windows Terminal,
- PowerShell,
- .NET,
- Windows Installer,
- Windows Recovery.

This is deliberately less aggressive than `tiny11core`.

## privacy-balanced profile

The privacy profile:

- disables the advertising ID,
- disables Windows consumer experiences,
- disables tailored experiences,
- disables silent suggested application delivery,
- limits diagnostics to required diagnostic data instead of breaking telemetry services,
- disables activity-feed publishing/upload,
- disables web suggestions in Windows Search for newly created users,
- applies policies disabling Recall data analysis and Windows Copilot,
- seeds privacy settings into the Default User profile.

It does **not** disable Windows Update, Defender, Microsoft Store or core networking services.

## Output

A successful build creates:

```text
Win11-OS11vLIN-Windows-11-Pro.iso
Win11-OS11vLIN-Windows-11-Pro.iso.sha256
```

The ISO also contains:

```text
/OS11vLIN-manifest.json
/sources/$OEM$/$$/Setup/Scripts/SetupComplete.cmd
/sources/$OEM$/$$/Setup/Scripts/OS11vLIN.ps1
```

After Windows installation, a copy of the manifest is placed under:

```text
C:\OS11vLIN\manifest.json
```

Provisioning logs are written to:

```text
C:\ProgramData\OS11vLIN\
```

## Validate an ISO

```bash
os11vlin validate ~/ISO/Win11-Pro-OS11vLIN.iso
```

Validation checks the ISO, selected `install.wim`, Windows setup boot image, injected scripts, manifest and El Torito boot metadata.

## Test in QEMU

UEFI/OVMF test:

```bash
os11vlin test ~/ISO/Win11-Pro-OS11vLIN.iso
```

Default VM:

- 2 vCPU,
- 4 GiB RAM,
- temporary 64 GiB disk,
- Q35,
- UEFI/OVMF,
- KVM automatically when available.

For example:

```bash
os11vlin test Win11-Pro-OS11vLIN.iso --memory 8192 --cpus 4 --disk 80
```

Legacy BIOS test:

```bash
os11vlin test Win11-Pro-OS11vLIN.iso --bios
```

The temporary test disk is deleted when QEMU exits.

## Build pipeline

```text
Microsoft Windows 11 ISO
        |
        v
extract install.wim/install.esd
        |
        v
wimlib reads all image indexes
        |
        v
choose Home / Pro / other
        |
        v
wimlib export selected index
        |
        +--> single-image install.wim
        |
        v
inject SetupComplete + tiny11-safe + privacy-balanced
        |
        v
xorriso rebuild using original boot metadata
        |
        v
validate ISO + manifest + boot metadata
        |
        v
SHA-256
        |
        v
optional QEMU/UEFI test
```

## Disk space

The builder temporarily extracts the source installation image and creates a selected-edition WIM. For modern Windows 11 media, having at least **15-20 GiB free** in the system temporary directory is recommended.

You can point temporary files elsewhere with standard Linux temporary-directory configuration, for example:

```bash
TMPDIR=/mnt/fastdisk/tmp os11vlin build Win11.iso
```

## Development tests

```bash
. .venv/bin/activate
pytest
```

GitHub Actions runs unit tests on Ubuntu and a Debian Trixie container. Real ISO boot/install validation should additionally be performed on Linux Mint, LMDE and Debian hosts because CI does not redistribute Microsoft installation media.

## Safety rules

1. The source ISO is never modified in place.
2. The source SHA-256 is checked again during the build.
3. A selected Windows image is exported into a new WIM rather than editing the source installation image.
4. Every modification is declared in a profile.
5. A build manifest is included in the result.
6. Critical Windows components are kept by the V1 profile.
7. The final ISO must pass structural validation before it is published as the output file.

## Legal note

OS11vLIN does not contain or redistribute Microsoft Windows binaries. Users provide their own installation ISO and are responsible for complying with the applicable Microsoft license terms.

## tiny11 relationship

OS11vLIN is an independent Linux-native builder inspired by the tiny11maker methodology. It is not an official tiny11/NTDEV project and deliberately uses a more conservative V1 package-removal policy.
