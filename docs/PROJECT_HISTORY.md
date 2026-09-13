# FX11 Builder — Project History

Purpose: persistent project memory kept in the repository so architectural decisions, checkpoints and implementation history do not depend on chat history.

## Working rule

From this point forward, every substantial FX11 decision or implementation step should be recorded here together with the relevant commit SHA(s). This file is the project checkpoint log; Git history remains the authoritative source for exact code changes.

## Canonical product decisions

- Product name: **FX11 OS**.
- Builder: **FX11 Builder**.
- Partitioning component: **FX Partition Manager**.
- Deployment component: **FX11 Installer**.
- Installed multi-OS menu: **FX Boot Manager**.
- Product principle: **Your System. Your Rules.** / **FX11 recommends; the user decides.**
- Windows remains installed in the standard `C:\Windows` path for compatibility and serviceability.
- Main Windows volume label: `FX11`.
- Product-facing directory: `C:\FX11`.
- Technical logs/state: `C:\ProgramData\FX11`.
- No hard-coded Windows user account. Normal Windows OOBE creates the user.

## Installation flow

Canonical flow:

`Boot USB/DVD -> FX Partition Manager -> FX11 Installer -> Windows image deployment -> FX Boot Manager -> Windows OOBE -> FX11 OS`

Responsibilities:

- FX Partition Manager discovers disks, prepares the selected layout and owns all partitioning decisions.
- FX11 Installer consumes the partition handoff context and installs to exactly that prepared target.
- FX11 Installer must not silently repartition or select another target.
- Deployment should use direct image application rather than depend on the stock Windows Setup compatibility gate.
- Stock `setup.exe` remains only as an explicit fallback path during development/recovery.

## Hardware compatibility policy

FX11 must not reject installation merely because Microsoft's stock Windows 11 compatibility gate considers the hardware unsupported.

FX11 should detect and display CPU/TPM/Secure Boot/RAM/security support, but treat those as advisory unless a capability is technically required by the selected FX11 deployment path.

Real blockers remain things such as inaccessible storage, wrong CPU architecture, insufficient target size, incompatible firmware/partition mode, failed image application or failed boot-file installation.

Rule: **warn, explain, allow when technically possible.**

## Partitioning

All partitioning modes are handled by FX Partition Manager, including Custom.

Guided modes:

- `FX11 only`
- `FX11 + Other OS`

Other OS space remains unallocated. FX11 does not assume Linux and does not create ext4/Btrfs/ZFS/UFS partitions in guided mode.

Normal automatic UEFI/GPT layout:

`EFI System -> MSR -> FX11 / Windows -> Windows Recovery`

Current guided constants:

- ESP: 300 MiB
- MSR: 16 MiB
- Recovery minimum: 1024 MiB
- Recovery free margin: 250 MiB
- FX11 guided Windows minimum: 64 GiB
- Other OS guided minimum: 16 GiB

Custom mode is staged/transactional. Delete/create/resize/format operations are proposals until final review and explicit commit. Existing partitions can be preserved.

Current implementation intentionally refuses ambiguous DiskPart resize generation; resize must be handled by a size-aware WinPE executor.

## Partition handoff

`src/fx11/install_context.py` defines `fx11-install-context-v1`.

The handoff records at least:

- selected physical disk,
- Windows/FX11 target partition,
- EFI System Partition,
- optional Recovery partition,
- preserved partitions,
- Other OS unallocated size,
- selected layout mode,
- acknowledged warnings.

ESP and Windows target must belong to the selected installation disk.

## FX Boot Manager

FX Boot Manager is GRUB-based and sits above native OS boot loaders.

For FX11:

`UEFI -> FX Boot Manager -> Windows Boot Manager -> FX11`

Existing EFI loaders should be preserved and chainloaded where possible. FX Boot Manager must not delete an existing UEFI entry just because it becomes the default.

Current development target:

- UEFI
- **Secure Boot OFF**
- unsigned GRUB payload

Future production target:

- Secure Boot ON
- trusted shim / signed chain
- signed FX GRUB

FX11 must never silently disable Secure Boot in firmware.

The boot manager will receive FX11 branding and a dedicated background/theme. User-configurable default OS, timeout and ordering are planned for FX11 Control Center.

## WinPE ownership

FX11 installation media is being changed so booting the media enters the FX11 flow rather than immediately handing control to stock Windows Setup.

Current bootstrap design:

`WinPE -> wpeinit -> FX11 launcher`

The development launcher is intentionally non-destructive and currently provides inspection/recovery options before destructive partitioning is connected.

Builder work now includes modifying `sources/boot.wim` and injecting:

- `Windows\System32\winpeshl.ini`
- `Windows\System32\startnet.cmd`
- `FX11\fx11-launch.cmd`

The intended final path is:

`WinPE -> FX Partition Manager -> handoff context -> FX11 Installer -> DISM /Apply-Image -> BCDBoot -> WinRE/OOBE`

## Security and audit decisions

- tiny11 is inspiration/reference only; FX11 is an independent Linux-native implementation.
- Do not execute mutable remote code during build.
- Do not introduce unverified executables.
- No hidden users, credentials, persistence or undeclared network behavior.
- Preserve Windows Update, Defender, SmartScreen, servicing and recovery unless the user explicitly chooses otherwise.
- Build manifest records source hashes, injected-file hashes and tooling provenance.
- `SetupComplete.cmd` verifies the SHA-256 of `FX11.ps1` before execution.
- Deep ISO/WIM audit exists, but runtime VM audit is still required for registry/services/tasks/users/firewall/certs/AppX/network state.

## Current implementation checkpoints

### Partitioning and handoff

- `fabcfb5eb287abb430ee4c39e64471cc10b013de` — Add safe UEFI GPT partition planning model
- `617df4d4b06216810d9bba5cf038e016debcbbc5` — Test FX11 partition planning safety rules
- `60552fca68e85bc9b98299752be3082743a68215` — Add custom partition planning model
- `bf1c0d6e29a3dde1b14700c4cd1dad2e54d406fd` — Harden custom resize execution
- `46751041ca49d6db3d8480cc7ab4aa5e9343ebbc` — Add partition manager installer handoff contract
- `d8d1bd6e8282744f3836ebf22b18c2dd5d08d0e5` — Test custom FX Partition Manager planning
- `1e9c2d57e1b6cb9e476882b2c3f828a3447b7191` — Test FX Partition Manager installer handoff

### Boot flow and compatibility

- `23967d8713dec11d8b19757f9a844b4b9601b46c` — Define FX Partition Manager boot flow before FX11 installation
- `296510738b6153a7cfaebac00b58ebf4748ed2e8` — Define compatibility and FX Boot Manager specification
- `d12a67eb29ba0377cc6a3eedba2ba32e501361fe` — Record Secure Boot development/production policy

### FX Boot Manager implementation

- `07088eccaaa6711366e572ff70ffca111de1a91e` — Add FX Boot Manager GRUB payload builder
- `03d9668c4975a17ae0d4fbec181123d045d773c4` — Test FX Boot Manager GRUB configuration
- `72d3c866684391f8ae0e10dc4fffa4a9f1bbeb5d` — Detect GRUB tooling for FX Boot Manager
- `237cfafa31864a961d080eb2ac8e3dd0e8c2ef3c` — Install GRUB UEFI build tooling
- `35361a2b2c659fc4d64864545304f54755d734ca` — Embed unsigned FX Boot Manager payload in FX11 ISO
- `2d09f16be529994b824aefd5bb1ffbc5133556fd` — Recognize FX Boot Manager payload in deep audit
- `f8115c6bfa81ae01bc141da19187c0770c2f536e` — Install GRUB UEFI tooling in CI smoke build

### WinPE ownership

- `c46c6a2eb31f604567d25815dfc1ae03ffb73c15` — Add FX11 WinPE bootstrap payload
- `a43b076987dbdf4d689f8602ec6eb6a2dd228e20` — Fix FX11 WinPE bootstrap launcher
- `b6e30d9ef87a05b37df2af8a057a22fce31f14df` — Test FX11 WinPE bootstrap payload
- `15f7f647dd22c5f169a38f434a4ee29b7b80d78d` — Customize Windows Setup boot.wim for FX11 startup
- `b3797ed77508d915c0a3c9e761af860cdbf316c5` — Inject FX11 launcher into boot.wim during build
- `6f8d3be723c0c30d7ca729ce9a68d82929b6bf7a` — Test boot.wim startup selection and injection plan
- `6d6e749e5d77d6c570b20988568f11c63309205b` — Verify FX11 WinPE handoff in synthetic build

### Audit/security

- `90eafc6a3533e303a3667a6d5ef45504ff502efb` — Add initial security audit and upstream tiny11 risk review
- `54db353e29168fc21c4aec65c681edcffd7f61b4` / `e7a6d33ccc7fd4218d9871889d1bdfebf057d2a5` — Provisioning integrity hardening
- `a713e932acdacd19843f11736fb480b671b8ecc7` — Add build-tool provenance and injected hashes to manifest
- `3f7ad640fff6c2fc476c434339d53bf09cac9a12` — Expand ISO audit with deep install image comparison
- `07b91cd7edd40cac72551dea7808ecd74cd9e895` — Deep audit CLI
- `323c7449573f9f2dc8153dba7e82bd8b31bca036` — Deep WIM audit tests

## Current checkpoint — 2026-09-13

Goal: produce a first real FX11 installation ISO from a genuine Microsoft Windows 11 ISO and boot it in UEFI with Secure Boot disabled.

Expected first visible checkpoint after boot:

`USB/DVD -> WinPE -> FX11 Installer / FX Partition Manager bootstrap`

Current development constraints:

- Secure Boot must be OFF for the current unsigned FX Boot Manager.
- The WinPE launcher is still a bootstrap, not the final graphical FX Partition Manager.
- No real Microsoft ISO has yet been declared successfully validated end-to-end in this project log.
- CI status is not authoritative for this checkpoint because the user intentionally stopped the latest CI run.
- Next authoritative checkpoint is local `pytest`, synthetic E2E, then a real Windows ISO build and QEMU/OVMF boot test.

## Next implementation steps

1. Complete and validate reliable `boot.wim` customization on a genuine Windows 11 ISO.
2. Boot the generated ISO in QEMU/OVMF and verify the FX11 WinPE handoff.
3. Replace the text bootstrap with the first usable FX Partition Manager front end.
4. Connect partition plan execution and write `fx11-install-context-v1`.
5. Implement direct image deployment (`DISM /Apply-Image`) to the prepared target.
6. Configure Windows boot files (`BCDBoot`), Recovery/WinRE and OOBE.
7. Install FX Boot Manager to the selected ESP after Windows boot files exist.
8. Add boot repair/recovery actions to the installation media.
9. Later: signed/trusted Secure Boot chain without changing the user-facing FX Boot Manager design.
