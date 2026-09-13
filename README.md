# FX11 Builder

> [!WARNING]
> **Status: TESTING / PRE-RELEASE**
>
> FX11 Builder is under active hardware and installer testing. The current `main` branch is intended for development and testing, not production use. Boot media, FX Partition Manager, the FX11 Installer handoff and the full installation flow are still being validated on real hardware.

FX11 Builder is a Linux-native Windows 11 image builder and installation-media project.

The project started from a simple observation: **tiny11/tiny11builder proved that a carefully trimmed Windows 11 can remain useful on hardware where the stock experience is unnecessarily heavy, but the available builder workflow is Windows/PowerShell-centric.** FX11 began as an attempt to build that kind of image reproducibly from Linux, and has since grown into a broader installation platform with its own partitioning, boot, privacy, audit and first-run design.

FX11 is an independent project. It is **not** an official tiny11, NTDEV or Microsoft project.

## Origin and acknowledgement

FX11 openly acknowledges **NTDEV / ntdevlabs tiny11builder** as the project that inspired the original direction.

Upstream reference:

- project: `ntdevlabs/tiny11builder`
- author/project family: NTDEV / tiny11
- role in FX11: conceptual and behavioral inspiration, research reference, comparison point

FX11 does not present the tiny11 ideas as its own invention. The original motivation was specifically: **tiny11 works well as a lightweight Windows concept; build a transparent, auditable Linux-native builder and then extend the installation experience beyond what tiny11builder provides.**

See `ACKNOWLEDGEMENTS.md` and `docs/THIRD_PARTY_COMPLIANCE.md` for the detailed attribution/compliance policy.

## How FX11 differs from tiny11builder

FX11 is not a port of the tiny11 PowerShell script. It is a separate implementation with a different architecture and different safety priorities.

Current or planned FX11 differences include:

- Linux-native build host instead of requiring Windows PowerShell/ADK as the primary builder environment,
- source Microsoft ISO is never modified in place,
- source and injected-file SHA-256 hashes recorded in a build manifest,
- conservative `tiny11-safe` removal profile rather than maximal stripping,
- Microsoft Defender, Windows Update, SmartScreen, Store, servicing and WinRE preserved by default,
- privacy-balanced policy separated from application removal,
- deep ISO/WIM audit and planned runtime VM audit,
- custom WinPE startup and direct Windows image deployment path,
- **FX Partition Manager**, with the main graphical line based on a properly attributed/branded GParted Live environment,
- our own text partition manager retained as recovery/fallback and as a development path,
- **FX Boot Manager** based on GRUB for multi-OS systems,
- unsupported-Windows-11 hardware treated as warn/explain/allow where technically possible instead of blindly reproducing stock Setup gating,
- planned FX11 First Run and FX11 Control Center,
- explicit multi-OS design (`FX11 + Other OS`) rather than assuming Linux-only dual boot.

The project principle is:

**Your System. Your Rules.**

and operationally:

**FX11 recommends; the user decides.**

## Current installation architecture

Target flow:

```text
Boot media
    |
    v
FX Partition Manager
    |-- main line: FX-branded GParted-based graphical environment
    |-- fallback: native FX text partition manager
    |
    v
installation handoff
    |
    v
FX11 Installer / WinPE
    |
    +--> apply selected Windows image
    +--> Windows boot files / WinRE / OOBE
    +--> FX Boot Manager payload
    |
    v
Windows OOBE
    |
    v
FX11 First Run
    |
    v
FX11 OS
```

The current development FX Boot Manager is unsigned and therefore the current milestone assumes **UEFI with Secure Boot disabled**. Production Secure Boot support is a later signing/trust-chain milestone.

## What the builder does today

- checks the Linux build host,
- reads Microsoft Windows 11 ISO files directly,
- supports `sources/install.wim` and `sources/install.esd`,
- lists Windows editions/indexes present in the source image,
- lets the user select an edition,
- exports the selected image with `wimlib` into a single-image `install.wim`,
- customizes `sources/boot.wim` so FX11 owns the WinPE startup path,
- injects the current FX11 provisioning payload,
- applies conservative AppX removal and privacy configuration,
- builds the development FX Boot Manager payload,
- preserves the source ISO boot structure through xorriso boot replay,
- validates the generated ISO,
- writes a build manifest and SHA-256 checksum,
- supports QEMU/OVMF testing from Linux.

The project is under active development. A real Microsoft ISO install must not be considered validated merely because synthetic tests pass.

## Current supported build hosts

The currently maintained bootstrap path targets:

- Linux Mint,
- LMDE,
- Debian.

These are the first supported hosts, not the intended final compatibility boundary.

### Host-distro roadmap

FX11 is intended to become progressively less tied to one Linux family. Planned work is to separate dependency detection from package-manager installation and add tested host adapters for additional distributions.

Likely next families include:

- Ubuntu-family systems,
- Fedora-family systems,
- openSUSE,
- Arch-family systems.

A distribution is only called **supported** after the full builder dependency/bootstrap/test path has actually been validated there.

## Possible future: FX Linux

If FX11 proves stable as a build/install platform, a future sibling project called **FX Linux** is planned for exploration.

FX Linux is not being defined as a rebadge of a particular distribution today. The idea is to reuse the useful FX principles and components — transparent choices, reproducible builds, FX Partition Manager, FX Boot Manager, multi-OS support, privacy controls and clear provenance — while keeping Linux licensing and upstream attribution explicit.

FX Linux should be a separate product/repository boundary rather than quietly turning FX11 Builder into an unrelated Linux distribution project.

## Why application removal currently happens during Windows provisioning

`wimlib` is excellent for reading, exporting and modifying WIM file contents, but it is not a complete replacement for Windows DISM servicing APIs.

FX11 therefore avoids blindly deleting component directories from an offline WIM. The transitional V1 path injects Windows provisioning that uses native Windows servicing interfaces for declared application removal. The longer-term installer architecture uses FX-controlled WinPE deployment while keeping Windows servicing assumptions intact.

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

## Inspect a source ISO

```bash
fx11 inspect ~/ISO/Win11.iso
```

FX11 reads the edition list from the actual `install.wim`/`install.esd`; it does not assume fixed image indexes.

## Build interactively

```bash
fx11 build ~/ISO/Win11.iso
```

Default profiles currently include:

```text
tiny11-safe
privacy-balanced
```

The `tiny11-safe` name intentionally acknowledges the historical inspiration; it does not mean the profile is copied verbatim from tiny11builder.

## Build non-interactively

By index:

```bash
fx11 build ~/ISO/Win11.iso --index 6 -o ~/ISO/Win11-Pro-FX11.iso
```

By edition name:

```bash
fx11 build ~/ISO/Win11.iso --edition "Windows 11 Pro"
```

By WIM EditionID:

```bash
fx11 build ~/ISO/Win11.iso --edition Professional
```

Use `--force` only when intentionally replacing an existing output ISO. FX11 refuses to overwrite the source ISO.

## Dry run and planning

```bash
fx11 build ~/ISO/Win11.iso --edition "Windows 11 Pro" --dry-run
fx11 plan
fx11 profiles
```

## tiny11-safe profile

The conservative profile removes selected consumer applications such as Clipchamp, News/Weather, Get Help/Get Started, People, Solitaire, Feedback Hub, Maps, Phone Link-related packages, consumer Xbox components, legacy media packages, consumer Teams, Family and Quick Assist.

It intentionally preserves Microsoft Store, Windows Update, Defender, SmartScreen, Edge/WebView2, Windows Terminal, PowerShell, .NET, Windows Installer and Windows Recovery.

The goal is not to win a smallest-ISO contest. The goal is a lighter Windows installation that remains serviceable and understandable.

## privacy-balanced profile

The privacy profile reduces optional telemetry/advertising/consumer-content behavior where it can be done without intentionally breaking normal servicing and security. Version-specific policies are treated cautiously because Windows behavior changes over time.

## Validate an ISO

```bash
fx11 validate ~/ISO/Win11-Pro-FX11.iso
```

## Test in QEMU

```bash
fx11 test ~/ISO/Win11-Pro-FX11.iso
```

QEMU/OVMF is used as the disposable first validation layer before real hardware.

## Development tests

```bash
. .venv/bin/activate
pytest
```

GitHub Actions runs automated tests and synthetic build checks. CI does not redistribute Microsoft installation media, so genuine Windows media still requires separate local/VM validation.

## Safety rules

1. The source ISO is never modified in place.
2. The source SHA-256 is checked again during the build.
3. A selected Windows image is exported into a new WIM rather than editing the user's source image in place.
4. Modifications should be declared and auditable.
5. A build manifest is included in the result.
6. Critical servicing/security components are kept by the default profile.
7. Third-party boot/runtime artifacts must be pinned and license-compliant.
8. The generated ISO must pass structural validation before being treated as a successful output.
9. Synthetic success is not called a real-Windows installation success.

## Third-party software and licensing

FX11 uses and/or plans to redistribute open-source components such as GRUB, wimlib, xorriso and a customized GParted Live environment. Each component remains subject to its own license.

The graphical partitioning experience is intended to be shown as:

**FX Partition Manager — powered by GParted**

FX branding must never erase upstream attribution or source/license obligations.

See `docs/THIRD_PARTY_COMPLIANCE.md`.

## Microsoft legal note

FX11 Builder does not contain or publish Microsoft Windows installation binaries as part of the source repository. Users provide their own Windows installation media and are responsible for complying with applicable Microsoft license terms.

## Project transparency

The repository deliberately records not only code but also project decisions and limitations:

- `docs/PROJECT_HISTORY.md` — canonical project memory,
- `docs/SECURITY_AUDIT.md` — security/audit decisions,
- `docs/THIRD_PARTY_COMPLIANCE.md` — third-party licensing/provenance policy,
- `docs/FX_PARTITION_MANAGER_GPARTED.md` — GParted-based partition-manager direction,
- `docs/TEST_HARDWARE.md` — reference real-hardware test systems.

If an upstream project materially influenced FX11, it should be acknowledged rather than hidden.
