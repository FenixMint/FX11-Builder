# FX11 Builder

FX11 Builder is a Linux-native Windows 11 ISO builder inspired by the tiny11maker approach, but designed around a conservative, serviceable build strategy.

It runs on Linux Mint, LMDE and Debian, keeps the original ISO untouched, lets you choose the exact Windows image contained in the ISO (Home, Pro, Pro N, Education, Enterprise, etc.), exports only that image into the new ISO, and applies `tiny11-safe + privacy-balanced` automatically during Windows Setup.

## What it does

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

`wimlib` is excellent for reading, exporting and modifying WIM file contents, but it is not a full replacement for Windows DISM servicing. FX11 Builder therefore does not blindly delete Windows component directories from a WIM.

Instead, the Linux builder prepares the image and injects a `SetupComplete` script. During Windows installation, Windows itself uses `Remove-AppxProvisionedPackage` and `Remove-AppxPackage` to remove declared applications. This keeps servicing safer than direct filesystem deletion.

## Installation on Mint / LMDE / Debian

```bash
git clone https://github.com/FenixMint/FX11-Builder.git
cd FX11-Builder
chmod +x scripts/bootstrap-debian.sh
./scripts/bootstrap-debian.sh
. .venv/bin/activate
```

Then verify the host:

```bash
fx11 doctor
```

The ISO builder itself requires `wimlib-imagex` and `xorriso`. QEMU/OVMF are optional and used for VM testing.

## Inspect a source ISO

```bash
fx11 inspect ~/ISO/Win11.iso
```

FX11 reads the edition list from the actual `install.wim`/`install.esd`; it does not assume fixed image indexes.

## Build interactively

```bash
fx11 build ~/ISO/Win11.iso
```

FX11 displays the available Windows images and asks for the image index.

Default profiles:

```text
tiny11-safe
privacy-balanced
```

## Build non-interactively

By index:

```bash
fx11 build ~/ISO/Win11.iso --index 6 -o ~/ISO/Win11-Pro-FX11.iso
```

By full edition name:

```bash
fx11 build ~/ISO/Win11.iso --edition "Windows 11 Pro"
```

By WIM EditionID:

```bash
fx11 build ~/ISO/Win11.iso --edition Professional
```

Use `--force` only when intentionally replacing an existing output ISO. FX11 always refuses to overwrite the source ISO.

## Dry run

```bash
fx11 build ~/ISO/Win11.iso --edition "Windows 11 Pro" --dry-run
```

You can also inspect profiles without creating an image:

```bash
fx11 plan
fx11 profiles
```

## tiny11-safe profile

The profile removes selected consumer applications such as Clipchamp, News and Weather, Get Help / Get Started, People, Solitaire, Feedback Hub, Maps, Phone Link, consumer Xbox packages, legacy media apps, consumer Teams, Family and Quick Assist.

It intentionally preserves Microsoft Store, Windows Update, Defender, SmartScreen, Edge/WebView2, Windows Terminal, PowerShell, .NET, Windows Installer and Windows Recovery.

## privacy-balanced profile

The privacy profile disables the advertising ID, Windows consumer experiences, tailored experiences, silent suggested application delivery, activity-feed publishing/upload, web suggestions for new users, and applies policies for Recall data analysis and Windows Copilot. Required diagnostic data remains enabled so servicing and security remain functional.

## Output

A successful default build creates a file similar to:

```text
Win11-FX11-Windows-11-Pro.iso
Win11-FX11-Windows-11-Pro.iso.sha256
```

The ISO also contains:

```text
/FX11-manifest.json
/sources/$OEM$/$$/Setup/Scripts/SetupComplete.cmd
/sources/$OEM$/$$/Setup/Scripts/FX11.ps1
```

After Windows installation, the manifest is copied to:

```text
C:\FX11\manifest.json
```

Provisioning logs are written to:

```text
C:\ProgramData\FX11\
```

## Validate an ISO

```bash
fx11 validate ~/ISO/Win11-Pro-FX11.iso
```

Validation checks the ISO, selected `install.wim`, Windows setup boot image, injected scripts, manifest and El Torito boot metadata.

## Test in QEMU

```bash
fx11 test ~/ISO/Win11-Pro-FX11.iso
```

Default VM:

- 2 vCPU,
- 4 GiB RAM,
- temporary 64 GiB disk,
- Q35,
- UEFI/OVMF,
- KVM automatically when available.

Example:

```bash
fx11 test Win11-Pro-FX11.iso --memory 8192 --cpus 4 --disk 80
```

Legacy BIOS:

```bash
fx11 test Win11-Pro-FX11.iso --bios
```

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
inject SetupComplete + build profiles
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

For modern Windows 11 media, at least **15–20 GiB free** in the temporary directory is recommended.

Example with a custom temporary directory:

```bash
TMPDIR=/mnt/fastdisk/tmp fx11 build Win11.iso
```

## Development tests

```bash
. .venv/bin/activate
pytest
```

GitHub Actions runs unit tests and a synthetic end-to-end multi-edition ISO build on Debian. Real Microsoft ISO boot/install validation should additionally be performed on Linux Mint, LMDE and Debian hosts because CI does not redistribute Microsoft installation media.

## Safety rules

1. The source ISO is never modified in place.
2. The source SHA-256 is checked again during the build.
3. A selected Windows image is exported into a new WIM rather than editing the source installation image.
4. Every modification is declared in a profile.
5. A build manifest is included in the result.
6. Critical Windows components are kept by the default profile.
7. The final ISO must pass structural validation before it is published as the output file.

## Legal note

FX11 Builder does not contain or redistribute Microsoft Windows binaries. Users provide their own installation ISO and are responsible for complying with the applicable Microsoft license terms.

## tiny11 relationship

FX11 Builder is an independent Linux-native builder inspired by the tiny11maker methodology. It is not an official tiny11/NTDEV project and deliberately uses a more conservative package-removal policy.
