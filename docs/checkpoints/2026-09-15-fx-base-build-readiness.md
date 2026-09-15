# FX Base — build readiness and product layering

Date: 2026-09-15

## Decision

FX is built as one common platform with two primary product paths:

```text
FX Base
├── FX Linux
└── FX11
```

FX Base is the shared Linux Live/build/runtime foundation. It is not a third competing desktop distribution edition. It provides the common boot, live environment, hardware/storage/network tooling, branding, launcher/orchestrator, Calamares framework and shared services required by both FX Linux and FX11.

### FX Linux

FX Linux is FX Base plus:
- selected desktop profile (Cinnamon first; MATE/KDE/TDE later),
- composable functional profiles (Multimedia, Gaming, Security/Pentest, Development, etc.),
- Linux installation path through Calamares,
- installed-system FX branding and configuration.

### FX11

FX11 is FX Base plus:
- FX11 installer/orchestrator profile,
- Windows-target partitioning and install-context handoff,
- reboot/transition to WinPE,
- FX11 phase-2 deployment frontend in WinPE,
- user-supplied Microsoft Windows media/payload.

Public FX Base / FX Linux media must not contain Microsoft Windows/WinPE binaries. A combined FX11/FX Linux hybrid containing Microsoft binaries is generated locally from user-supplied Windows media.

## Branding rule

The product is FX. Upstream projects remain credited, but the user-facing product must not present itself as Linux Mint or LMDE.

The first visible screen is FX-branded boot UI. Upstream GRUB may remain the engine, but the menu/theme/entries are FX-owned user experience.

## Source image selected

LMDE 7 Cinnamon 64-bit source image has been fingerprinted and inspected. The shared Live payload is based on:
- `/live/filesystem.squashfs`
- `/live/vmlinuz`
- `/live/initrd.lz`

Boot paths:
- BIOS: `/isolinux/live.cfg`
- UEFI: `/boot/grub/grub.cfg`

Both boot the same Live system and can carry the FX mode contract:
- `fx.mode=windows`
- `fx.mode=linux`
- `fx.mode=live`

## What is still needed before the first real FX Base build

Only a small number of implementation contracts need to be fixed. They should not block beginning the PoC.

1. **FX Base identity contract**
   - User-facing name: FX / FX Base.
   - Upstream provenance remains documented.
   - Do not change low-level distro-identification fields blindly if doing so can break package/detection logic; validate `/etc/os-release` strategy before hard-locking it.

2. **Common filesystem overlay**
   - FX boot branding and theme.
   - FX launcher/orchestrator.
   - shared assets and configuration.
   - Calamares profiles/configuration.
   - mode-routing service/script.

3. **Package manifests**
   - base packages shared by both products,
   - FX Linux-only packages,
   - FX11-only packages,
   - later composable functional profiles.

4. **Build reproducibility**
   - source ISO SHA256 is pinned,
   - build script records source fingerprint, repo commit and resulting ISO SHA256,
   - no manual-only changes inside a one-off chroot.

5. **Acceptance criteria for the first image**
   - boots on UEFI physical hardware,
   - FX-branded GRUB is the first product UI,
   - all three mode entries reach the same FX Base Live rootfs,
   - `fx.mode` is visible inside the running Live system,
   - FX launcher routes correctly,
   - no destructive installer action is required for the first boot PoC.

## Recommended first implementation milestone

Build **FX Base PoC 1**, deliberately small:

```text
FX GRUB
  ├── Install FX11       -> fx.mode=windows
  ├── Install FX Linux   -> fx.mode=linux
  └── Try FX / Tools     -> fx.mode=live
            |
            v
       one FX Base Live
            |
            v
       FX launcher
```

Do not yet attempt a complete FX Linux installation or Windows deployment in the same milestone. First prove the common base, branding and routing. Once that is stable, branch functionality above the same foundation.

## Build order

1. FX Base PoC 1: boot + branding + mode routing.
2. FX Linux PoC: Calamares Linux install path from the same base.
3. FX11 Linux-phase PoC: partition/orchestration + durable handoff.
4. FX11 WinPE phase 2.
5. Locally generated FX hybrid media from user-supplied Windows ISO.

This layering is the canonical direction unless later testing demonstrates a technical reason to change it.
