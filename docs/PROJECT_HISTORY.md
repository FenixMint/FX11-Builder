# FX11 Builder — Project History and Canonical Decisions

Purpose: persistent project memory kept in the repository so architectural decisions, product decisions, implementation checkpoints, small UX choices, constraints, open questions and known limitations do not depend on chat history.

## Working rule

This file is the canonical project memory for FX11. From now on, every meaningful decision — large or small — should be recorded here together with the relevant implementation checkpoint or commit when applicable.

Git history remains authoritative for exact code changes. This document is authoritative for *why* the project behaves the way it does and what has already been agreed.

When a later decision supersedes an older one, the newer decision must be recorded here explicitly instead of silently replacing history.

---

# 1. Project identity and boundaries

## Product names

- Operating system/product experience: **FX11 OS**.
- Builder: **FX11 Builder**.
- Partitioning component: **FX Partition Manager**.
- Deployment component: **FX11 Installer**.
- Installed multi-OS boot menu: **FX Boot Manager**.
- First-login configuration experience: **FX11 First Run**.
- Post-install management application: **FX11 Control Center**.

## Brand principles

Primary product line:

- **FX11 OS for you**
- **Your System. Your Rules.**

Product behavior rule:

- **FX11 recommends; the user decides.**

FX11 should explain consequences and recommend safe defaults, but recommendations must not silently become restrictions unless the restriction is required for integrity, bootability or data safety.

Suggested product choice levels:

- **Required**
- **Recommended by FX11**
- **Available**
- **Advanced**

## Project boundary

FX11 Builder is a separate project from **FX Nexus**. The two must not be mixed conceptually, in naming, packaging or repository logic.

---

# 2. Filesystem and installed-system identity

Windows remains installed in the standard:

`C:\Windows`

Reason: compatibility, servicing, updates, application assumptions and recovery behavior.

FX11 does **not** relocate Windows itself into `C:\FX11`.

Instead:

- Windows system directory: `C:\Windows`
- Main Windows volume label: **FX11**
- Product-visible FX11 directory: `C:\FX11`
- Technical logs/state/configuration: `C:\ProgramData\FX11`

Explorer should therefore naturally show the system volume as something equivalent to:

`FX11 (C:)`

No hard-coded developer account, local user or default admin account is created by FX11.

Normal Windows OOBE creates the user after deployment.

Default User profile settings may be staged, but this must never be used to create an account implicitly.

---

# 3. Canonical installation flow

Final intended flow:

`Boot USB/DVD -> FX Partition Manager -> FX11 Installer -> Windows image deployment -> FX Boot Manager -> Windows OOBE -> FX11 First Run -> FX11 OS`

Responsibilities are strictly separated.

## FX Partition Manager owns

- disk discovery,
- disk selection,
- guided layouts,
- Custom mode,
- destructive-operation confirmation,
- resize planning,
- partition-role assignment,
- final partition execution,
- creating the installation handoff context.

## FX11 Installer owns

- reading the partition handoff,
- applying the selected Windows image to the prepared FX11 target,
- preparing Microsoft Windows boot files,
- configuring Recovery / WinRE when selected,
- preparing OOBE,
- installing/configuring FX Boot Manager on the selected ESP,
- never asking the user to repeat partition selections already made in FX Partition Manager.

FX11 Installer must not silently repartition, silently choose another disk or silently select another ESP.

If partition validation or partition execution fails, deployment must not start.

---

# 4. Windows 11 hardware compatibility policy

FX11 must **not** copy Microsoft's stock Windows 11 hardware gate as an installation blocker.

FX11 should detect and display the following information:

- CPU support status,
- TPM presence/version,
- Secure Boot state,
- RAM,
- storage,
- virtualization/security features,
- architecture compatibility.

However these are advisory unless they are genuinely required by the selected FX11 deployment path.

Examples that should be shown as warnings rather than blockers where technically possible:

- CPU generation/model not on Microsoft's supported list,
- TPM absent or below Microsoft's normal Windows 11 requirement,
- Secure Boot disabled,
- RAM below Microsoft's ordinary Windows 11 recommendation,
- security/virtualization capabilities not present.

Examples of genuine blockers:

- wrong CPU architecture for the selected image,
- selected target inaccessible,
- selected target too small to hold the image,
- image cannot be applied,
- boot files cannot be installed,
- selected firmware/partition scheme is incompatible with the requested installation path.

Rule:

**Warn, explain, allow when technically possible.**

FX11 must distinguish clearly between:

- Microsoft Windows 11 officially supported hardware,
- FX11 installation technically possible,
- FX11 recommendation/warning.

FX11 must not promise that unsupported hardware will receive every future Windows update or future driver.

---

# 5. Deployment method

The preferred deployment architecture avoids relying on stock `setup.exe` for the actual installation.

Target implementation:

`WinPE -> FX Partition Manager -> FX11 Installer -> DISM /Apply-Image -> BCDBoot -> WinRE/OOBE`

Reasons:

- FX11 controls target selection,
- Microsoft's stock hardware compatibility gate does not become authoritative,
- partition layout does not need to be reselected,
- deployment becomes deterministic and easier to audit.

Stock Windows Setup remains only as an explicit fallback/recovery option during development or special cases.

Compatibility-bypass registry values may exist later only as a fallback when FX11 intentionally invokes Microsoft Setup. They are not the primary design.

---

# 6. FX Partition Manager — global behavior

All partitioning modes are handled by **FX Partition Manager**, including **Custom**.

The stock Windows partition screen is not the normal destination for Custom mode.

FX11 should help the user understand what Windows/FX11 needs while still providing full control.

## Guided modes

- **FX11 only**
- **FX11 + Other OS**

The term **Other OS** is canonical.

Do not rename the slider or option to `Linux`.

Explanatory examples may include Linux, BSD and other operating systems.

## Other OS space

In guided `FX11 + Other OS` mode, FX11 leaves the second-system space **unallocated**.

FX11 does not create:

- ext4,
- Btrfs,
- ZFS,
- UFS,
- swap,
- `/home`,
- BSD-specific layouts.

The future OS owns its own partitioning.

## Automatic UEFI/GPT layout

Canonical guided layout:

`EFI System -> MSR -> FX11 / Windows -> Windows Recovery`

Current constants:

- ESP: **300 MiB**
- MSR: **16 MiB**
- Recovery minimum: **1024 MiB**
- Recovery free margin: **250 MiB**
- FX11 guided Windows minimum: **64 GiB**
- Other OS guided minimum: **16 GiB**

Normal automatic target is UEFI + GPT.

Legacy BIOS/MBR is not the standard automatic layout.

## Custom mode

Custom mode is fully managed by FX Partition Manager.

It should show:

- graphical disk map,
- partition table,
- filesystem/type,
- partition size,
- used/free space where reliably detectable,
- detected OS/role when reliable,
- EFI System role,
- MSR role,
- Windows role,
- Recovery role,
- data partitions,
- unallocated space.

Supported actions where technically safe:

- Create partition
- Delete partition
- Resize partition
- Format partition
- Leave unallocated
- Preserve unchanged
- Use as FX11
- Use as EFI System Partition
- Use as Recovery

## Custom status labels

UI should distinguish:

- Required for FX11
- Recommended by FX11
- Optional
- Existing / preserved
- Warning
- Invalid for this installation

## Staged/transactional changes

Custom mode is staged.

Create/delete/resize/format operations initially change only the proposed plan.

The disk is not changed until final review and explicit commit.

The UI should distinguish:

- current,
- new,
- deleted,
- resized,
- formatted,
- preserved,
- unallocated.

Undo must be available before commit.

Final review should show:

`Current layout -> Proposed layout`

Suggested destructive confirmation text:

`I have reviewed the listed disk changes and understand which partitions may lose data.`

Suggested whole-disk action:

`Erase selected disk and create this layout`

Suggested custom action:

`Apply these partition changes`

## Multiple disks

Guided modes affect only the explicitly selected disk.

Custom mode may inspect/modify additional physical disks intentionally, but FX11 must never automatically select another physical disk.

## Resize safety

Current implementation deliberately refuses ambiguous DiskPart resize generation.

Resize must be handled by a size-aware WinPE executor that understands source and target sizes correctly.

Do not reintroduce `shrink desired=<target size>` style logic as a shortcut.

---

# 7. Partition handoff contract

`src/fx11/install_context.py` defines:

`fx11-install-context-v1`

The context records at least:

- layout mode,
- selected physical disk number,
- physical disk model,
- disk size,
- selected Windows/FX11 target partition,
- selected EFI System Partition,
- optional Recovery partition,
- preserved partitions,
- Other OS unallocated size,
- acknowledged warnings.

Windows target and ESP must belong to the selected installation disk.

Recovery, when selected, must also belong to that disk.

FX11 Installer consumes this context and must not silently reinterpret it.

---

# 8. FX Boot Manager

FX Boot Manager is a **GRUB-based** top-level multi-OS menu.

For FX11:

`UEFI -> FX Boot Manager -> Windows Boot Manager -> FX11`

Windows' own BCD/boot logic remains in place underneath FX Boot Manager.

Existing OS loaders should be chainloaded rather than replaced where possible.

FX Boot Manager should detect entries from evidence such as:

- UEFI NVRAM entries,
- EFI executables on detected ESPs,
- partition metadata,
- existing bootloader metadata,
- safe os-prober-style discovery.

If the OS identity cannot be determined reliably, show loader/path information instead of inventing a name.

Existing boot entries must be preserved.

Becoming first in firmware boot order must not imply deleting other entries.

## Current development Secure Boot mode

For the current development milestone:

- UEFI
- **Secure Boot OFF**
- unsigned GRUB-based FX Boot Manager

FX11 must detect Secure Boot state.

If Secure Boot is ON while using the unsigned development boot manager, FX11 must not install it blindly.

User options should include:

- disable Secure Boot manually in firmware,
- continue with Windows Boot Manager only,
- return/cancel.

FX11 must never silently alter firmware Secure Boot state.

## Future production Secure Boot target

Target architecture:

`UEFI Secure Boot ON -> trusted/signed shim -> signed FX GRUB -> selected OS`

The user-facing FX Boot Manager design should stay the same when the signing chain changes.

Signing/trust is an external production milestone and is not considered completed today.

## Theme and branding

FX Boot Manager will have:

- FX11 background/wallpaper,
- FX branding,
- readable large OS names,
- visible selected-entry highlight,
- keyboard navigation,
- configurable timeout,
- graphics fallback to text mode.

Default OS after fresh FX11 install: **FX11**.

Suggested default timeout: **5 seconds**.

Later FX11 Control Center should allow changing:

- default OS,
- timeout,
- ordering,
- visible entries,
- theme/background where supported.

## Boot repair

Installation media should later include boot repair functions:

- reinstall FX Boot Manager,
- regenerate menu entries,
- rebuild/reinstall Windows Boot Manager for FX11,
- choose another detected loader as firmware default,
- inspect UEFI entries,
- inspect ESP contents before changes.

FX Boot Manager must not become a single point of failure.

---

# 9. WinPE ownership

FX11 installation media should boot into the FX11 flow rather than immediately launching ordinary Windows Setup.

Current startup chain:

`WinPE -> wpeinit -> FX11 launcher`

Builder work now modifies `sources/boot.wim` and injects:

- `Windows\System32\winpeshl.ini`
- `Windows\System32\startnet.cmd`
- `FX11\fx11-launch.cmd`

The current bootstrap is intentionally non-destructive.

It exists to prove:

- FX11 controls WinPE startup,
- devices/network can initialize through `wpeinit`,
- the user reaches FX11 before stock Setup,
- fallback recovery paths remain available.

Current development launcher options include inspection/command-line/fallback Setup/reboot.

The final GUI replaces this text bootstrap.

---

# 10. Desktop visual identity

## Main desktop concept

Default wallpaper concept: **FX11 Lazur**.

Visual direction:

- turquoise/azure tropical sea,
- tiny sandy island,
- palm trees,
- deep blue sky,
- white clouds,
- sailboat on the right.

Do not drift into a Windows XP Bliss-style green hill composition.

## Start button

Start button uses the **FX mark only**.

Do not use:

- Windows logo,
- the word `Start`.

## Taskbar

Default taskbar position: **top**.

Long-term target is user-selectable:

- top,
- bottom,
- left,
- right,

where the selected shell/Windows build supports it safely.

Prefer native Windows capabilities where available instead of unnecessary shell patching.

## Start menu styles

Target selectable styles:

- Windows XP-inspired
- Windows 7-inspired
- Windows 10-inspired
- Windows 11

Configuration later lives in FX11 Control Center.

Candidate shell tooling researched:

- Open-Shell for XP/Windows 7 style possibilities,
- ExplorerPatcher for Windows 10-like behavior where compatible.

Do not invent unsupported automation for custom ExplorerPatcher Start buttons.

---

# 11. Windows OOBE and FX11 First Run

No user account is created in advance.

Normal Windows OOBE happens first.

Only after OOBE and first sign-in does **FX11 First Run** start.

First Run target sections:

- Welcome
- Privacy explanation
- Start menu style
- Taskbar position
- Recommended browser selection
- Optional applications
- Privacy / Proton options
- Optional WSL2

Partitioning is **not** part of First Run.

Each optional app should include a short explanation of why it may be useful.

Nothing optional should be silently installed.

FX11 should encourage at least one recommended browser but must not force one.

Third-party software should preferably be downloaded in a current version from its normal vendor/package source at install time instead of embedding stale binaries.

---

# 12. Recommended applications

## Browsers

Recommended/available set:

- LibreWolf
- Firefox
- DuckDuckGo Browser
- Brave
- Thorium
- SRWare Iron

Chrome is not a recommended/default FX11 browser, but FX11 does not block its installation.

## Mail

- Thunderbird

## Office

- LibreOffice — strongly recommended

## PDF

- SumatraPDF
- PDFsam Basic
- LibreOffice Draw
- optional Stirling-PDF

## Archives

- 7-Zip
- PeaZip

## Drivers

- Driver Booster may be offered as an optional tool
- it must not silently override Windows Update/OEM driver policy

## VC++ runtime

Current supported Microsoft Visual C++ Redistributable must be verified/installed for:

- x86
- x64

This is treated as a mandatory compatibility/runtime check, not a random optional app.

Use official Microsoft sources and verify current URLs before hardcoding evergreen links.

---

# 13. Proton and privacy-oriented apps

Optional Proton-related offerings may include:

- Proton VPN
- Proton Pass
- Proton Drive
- Proton Mail / Calendar

Do not misrepresent plan limitations.

In particular, Proton Mail desktop availability may depend on paid/trial conditions and should not be presented as universally free.

---

# 14. WSL2 and Linux integration

WSL2 is optional.

If the user does not select WSL2, FX11 does not enable WSL/virtualization features just because they exist.

Recommended WSL distributions when available in the current Microsoft WSL catalogue:

- Fedora
- Debian
- AlmaLinux

Ubuntu may still be shown if present because the user decides, but it should not be promoted/preselected/auto-installed by FX11.

FX11 should query the live catalogue, e.g. equivalent to:

`wsl --list --online`

or:

`wsl -l -o`

Never use bare:

`wsl --install`

because that can implicitly install the current default distribution.

Preferred pattern where supported:

- enable WSL infrastructure without a distribution,
- install the exact distribution selected by the user.

---

# 15. Other OS / multi-OS terminology

Canonical wording:

- **FX11 + Other OS**
- slider: **FX11** <-> **Other OS**
- documentation/module: **Multi-OS Guide**

Do not call the guide `Dual Boot Guide`, because the user may have more than two operating systems.

Do not assume the second system is Linux.

Examples may mention Linux and BSD, but terminology remains Other OS.

---

# 16. FX11 Control Center

Planned primary sections:

- Appearance
- Start & Taskbar
- Applications
- Privacy
- Linux / WSL2
- Multi-OS Guide
- Windows
- Updates
- FX11 Status

Privacy module should include a future action equivalent to:

`Privacy Check / Restore FX11 Privacy`

Boot-manager configuration should eventually integrate here as well.

---

# 17. Privacy policy

FX11 aims for a privacy-balanced Windows configuration.

Target areas to disable/restrict where safe:

- optional telemetry,
- Windows Error Reporting uploads,
- feedback prompts,
- CEIP-style participation,
- Activity History upload,
- Advertising ID,
- tailored experiences,
- sponsored/consumer content,
- unnecessary telemetry-related tasks/services where safe,
- search/content suggestions,
- AI/Copilot/Recall-related policy where version-appropriate and technically reliable.

Core components to preserve by default:

- Windows Update
- activation
- Microsoft Defender
- SmartScreen
- Store unless a profile explicitly changes it
- core networking
- servicing
- recovery

Privacy recommendations must not break normal servicing unnecessarily.

---

# 18. Current builder architecture

FX11 Builder is Linux-native.

Current V1 strategy:

- source Microsoft ISO is never modified in place,
- source SHA-256 is recorded and rechecked,
- selected Windows edition is exported into a new single-image WIM,
- build manifest records source, tools and injected files,
- xorriso replays original boot metadata,
- output ISO is structurally validated,
- QEMU/UEFI test command exists.

Linux cannot fully replace Windows DISM servicing APIs in every area.

Current V1 therefore uses wimlib for image inspection/export and applies declared AppX/privacy actions later through:

`$OEM$\$$\Setup\Scripts\SetupComplete.cmd`

which verifies and launches:

`FX11.ps1`

The current SetupComplete strategy is a transitional implementation; the direct WinPE deployment architecture remains the longer-term installation path.

---

# 19. App/debloat policy

Protected components include:

- Microsoft Store
- Windows Update
- Microsoft Defender
- SmartScreen
- WinRE
- Windows Installer
- PowerShell
- .NET
- WebView2
- Microsoft Edge
- Windows Terminal

Current `tiny11-safe` removal targets include items such as:

- Clipchamp
- Bing News
- Bing Weather
- Get Help
- Get Started
- People
- Solitaire
- Feedback Hub
- Maps
- Your Phone / Phone Link-related package
- Xbox consumer components
- Zune Music/Video legacy packages
- Teams consumer package
- Family
- Quick Assist

The goal is not maximal stripping at all costs. Serviceability and recovery take priority over headline ISO size.

---

# 20. Security model

Tiny11/tiny11builder is inspiration/reference only.

FX11 is an independent Linux-native implementation.

Project security rules:

- no mutable remote code execution during build,
- no unverified downloaded executables,
- no hidden local users,
- no hidden credentials,
- no hidden persistence,
- no undeclared network behavior,
- manifest all injected content,
- preserve Defender/SmartScreen/Windows Update/recovery by default,
- test builds in disposable VMs before real hardware.

Known upstream/tiny11 risk examples that motivated this policy include:

- downloading mutable `main` content,
- downloading executable tooling without pinned expected hashes,
- privileged PowerShell,
- Core variants that deliberately disable Defender/Windows Update.

These are not FX11 design goals.

---

# 21. Provisioning integrity

FX11 build computes SHA-256 of `FX11.ps1`.

`SetupComplete.cmd` embeds the expected hash and verifies the script before executing it.

A mismatch must stop the provisioning script and log a security error.

Build manifest records:

- source ISO hash,
- injected file hashes,
- build-tool paths,
- build-tool versions where available.

Current PowerShell invocation still uses an execution-policy bypass as part of the setup execution path; this remains a security-sensitive implementation detail to validate in the real-Windows runtime audit.

---

# 22. Audit model

Static ISO/WIM audit exists.

Current deep audit includes:

- ISO filesystem inventory,
- added/removed/common paths,
- expected FX11 additions,
- source/output install image extraction,
- selected-image inventory comparison,
- WIM metadata comparison,
- injected file hashes,
- manifest inspection.

Current schema:

`fx11-iso-delta-v2`

Important limitation:

Path inventory equality does not prove byte-for-byte equality of every WIM file payload.

Runtime VM audit is still required for:

- registry changes,
- services/start modes,
- scheduled tasks,
- Run/RunOnce/startup,
- firewall rules,
- Defender/SmartScreen,
- certificates/trusted roots,
- local users/groups,
- drivers,
- AppX inventory,
- network destinations during Setup/OOBE/First Run.

A future forensic mode may hash selected/all WIM payloads if performance is acceptable.

---

# 23. VM/test direction

Disposable VM testing is part of the security and validation model.

QEMU/OVMF is the current Linux-side test direction.

Known VM areas still needing hardening:

- proper writable OVMF VARS handling,
- virtual TPM / swtpm,
- SATA/AHCI choice for vanilla Windows visibility,
- avoid depending on virtio storage unless drivers are explicitly present,
- e1000e is a safer initial network model than requiring virtio-net drivers.

Do not claim a real Windows install is validated until it has actually booted and completed the intended checkpoint.

---

# 24. Branding assets and visual checkpoints

Previously generated design checkpoints exist for:

- metallic FX/FX11 logo concepts,
- Lazur tropical wallpaper concept,
- polished FX11 desktop concept,
- revised FX-only Start button concept.

Canonical visual direction remains:

- FX-only Start mark,
- no Windows logo on the FX Start button,
- Lazur tropical wallpaper,
- XP-inspired taskbar feel with modern usability,
- clear FX branding without pretending Windows is a different underlying kernel/product family.

Windows 11 foundation/build information should remain transparent in diagnostics/about information.

---

# 25. Known current limitations

As of the current checkpoint:

- no real Microsoft Windows 11 ISO has yet been declared fully validated end-to-end in this project history,
- split WIM support is not yet confirmed/implemented as a finished path,
- synthetic xorriso replay is tested more than real-Microsoft-media replay,
- SetupComplete behavior still requires real Windows validation,
- Home edition may ignore some policy-based privacy settings,
- Windows Update may reprovision some consumer apps,
- AI/Copilot/Recall policy details may change with Windows versions,
- current FX Boot Manager payload is unsigned and therefore development target is Secure Boot OFF,
- final graphical FX Partition Manager is not yet complete,
- resize executor is intentionally not finished,
- runtime VM security audit is still pending,
- signed Secure Boot chain is a later production milestone.

---

# 26. Implementation checkpoints

## Product specification / naming

- `0db7eeb73c5e9f8d1e3b844aefa6b1de2c79ac14` — Full internal rename to FX11
- `30242559600be10f4ea748be14551c197a36cc55` — Record user-choice product principle

## Partitioning and handoff

- `fabcfb5eb287abb430ee4c39e64471cc10b013de` — Add safe UEFI GPT partition planning model
- `617df4d4b06216810d9bba5cf038e016debcbbc5` — Test FX11 partition planning safety rules
- `8f2b3f8a253d81dd87b905deeb092922ecbce997` — Define FX11 automatic UEFI GPT partitioning rules
- `26f8031388a41a751f93a5dafe0f2f1f147111de` — Make Custom partitioning fully managed by FX11 flow (older terminology later superseded by FX Partition Manager naming)
- `60552fca68e85bc9b98299752be3082743a68215` — Add custom partition planning model
- `bf1c0d6e29a3dde1b14700c4cd1dad2e54d406fd` — Harden custom resize execution
- `46751041ca49d6db3d8480cc7ab4aa5e9343ebbc` — Add partition manager installer handoff contract
- `d8d1bd6e8282744f3836ebf22b18c2dd5d08d0e5` — Test custom FX Partition Manager planning
- `1e9c2d57e1b6cb9e476882b2c3f828a3447b7191` — Test FX Partition Manager installer handoff
- `23967d8713dec11d8b19757f9a844b4b9601b46c` — Define FX Partition Manager boot flow before installation

## Compatibility / boot manager specification

- `296510738b6153a7cfaebac00b58ebf4748ed2e8` — Define compatibility and FX Boot Manager specification
- `d12a67eb29ba0377cc6a3eedba2ba32e501361fe` — Record Secure Boot development/production policy

## FX Boot Manager implementation

- `07088eccaaa6711366e572ff70ffca111de1a91e` — Add FX Boot Manager GRUB payload builder
- `03d9668c4975a17ae0d4fbec181123d045d773c4` — Test FX Boot Manager GRUB configuration
- `72d3c866684391f8ae0e10dc4fffa4a9f1bbeb5d` — Detect GRUB tooling for FX Boot Manager
- `237cfafa31864a961d080eb2ac8e3dd0e8c2ef3c` — Install GRUB UEFI build tooling
- `35361a2b2c659fc4d64864545304f54755d734ca` — Embed unsigned FX Boot Manager payload in FX11 ISO
- `2d09f16be529994b824aefd5bb1ffbc5133556fd` — Recognize FX Boot Manager payload in deep audit
- `f8115c6bfa81ae01bc141da19187c0770c2f536e` — Install GRUB UEFI tooling in CI smoke build

## WinPE ownership

- `c46c6a2eb31f604567d25815dfc1ae03ffb73c15` — Add FX11 WinPE bootstrap payload
- `a43b076987dbdf4d689f8602ec6eb6a2dd228e20` — Fix FX11 WinPE bootstrap launcher
- `b6e30d9ef87a05b37df2af8a057a22fce31f14df` — Test FX11 WinPE bootstrap payload
- `15f7f647dd22c5f169a38f434a4ee29b7b80d78d` — Customize Windows Setup boot.wim for FX11 startup
- `b3797ed77508d915c0a3c9e761af860cdbf316c5` — Inject FX11 launcher into boot.wim during build
- `6f8d3be723c0c30d7ca729ce9a68d82929b6bf7a` — Test boot.wim startup selection and injection plan
- `6d6e749e5d77d6c570b20988568f11c63309205b` — Verify FX11 WinPE handoff in synthetic build

## Audit/security

- `90eafc6a3533e303a3667a6d5ef45504ff502efb` — Add initial security audit and tiny11 risk review
- `54db353e29168fc21c4aec65c681edcffd7f61b4` / `e7a6d33ccc7fd4218d9871889d1bdfebf057d2a5` — Provisioning integrity hardening
- `a713e932acdacd19843f11736fb480b671b8ecc7` — Add build-tool provenance and injected hashes to manifest
- `4e1cb6901c0c0315b092e42c8fbd84a89bb7cd50` — Initial audit implementation
- `d17c849aebb74016e80035be7fec99ade6d3b5dc` — Add audit CLI
- `2b1f5c2a29b406579b103a142951b046f6dcfd62` — Add audit tests
- `ad80e5e8904528714a9592ff6d5a25d00f094976` — Add provisioning integrity tests
- `3f7ad640fff6c2fc476c434339d53bf09cac9a12` — Expand ISO audit with deep install image comparison
- `07b91cd7edd40cac72551dea7808ecd74cd9e895` — Deep audit CLI
- `323c7449573f9f2dc8153dba7e82bd8b31bca036` — Deep WIM audit tests

## Persistent project history

- `2653c1c60dab59ba535523a2e228a01aa60565a4` — Create persistent project history file

---

# 27. Current checkpoint — 2026-09-13

Immediate goal:

Produce the first real FX11 installation ISO from a genuine Microsoft Windows 11 ISO and boot it in UEFI with Secure Boot disabled.

Expected first visible checkpoint:

`USB/DVD -> WinPE -> FX11 Installer / FX Partition Manager bootstrap`

Current authoritative validation sequence:

1. local environment/bootstrap,
2. `fx11 doctor`,
3. local `pytest`,
4. synthetic E2E build,
5. real Microsoft Windows ISO inspection/build,
6. QEMU/OVMF boot,
7. confirm that FX11 owns WinPE startup,
8. only then connect destructive partition execution and direct deployment.

The latest CI run was intentionally stopped by the user and is therefore not the authoritative checkpoint.

---

# 28. Next implementation order

1. Complete/revalidate `boot.wim` customization against a genuine Windows 11 ISO.
2. Boot generated ISO in QEMU/OVMF with Secure Boot OFF.
3. Confirm FX11 launcher appears instead of normal Windows Setup.
4. Replace bootstrap launcher with first usable FX Partition Manager UI.
5. Add reliable disk inventory and role detection.
6. Connect guided partition execution.
7. Implement safe Custom execution including resize.
8. Write `fx11-install-context-v1` from the completed partition layout.
9. Implement direct Windows deployment with `DISM /Apply-Image`.
10. Configure Windows boot files with `BCDBoot`.
11. Configure WinRE/Recovery when present.
12. Prepare OOBE.
13. Install FX Boot Manager to selected ESP.
14. Detect/preserve existing OS loaders and create menu entries.
15. Add boot repair/recovery tools.
16. Implement FX11 First Run.
17. Implement FX11 Control Center.
18. Later: production Secure Boot signing/trust chain.
19. Add full runtime VM security audit and clean-vs-FX11 comparison.

---

# 29. Documentation maintenance rule

This file should be updated whenever any of the following changes:

- product naming,
- UX wording,
- default values,
- partition sizes/layout,
- supported installation mode,
- Secure Boot policy,
- boot flow,
- app recommendations,
- privacy behavior,
- WSL behavior,
- desktop defaults,
- security assumptions,
- build dependencies,
- runtime limitations,
- test/validation status,
- major implementation checkpoint,
- decision superseding an earlier decision.

Small decisions matter too. If they could affect implementation later, they belong here.
