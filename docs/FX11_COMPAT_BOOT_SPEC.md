# FX11 Compatibility and Boot Manager Specification

Status: implementation baseline for FX11 Installer.

This document defines two product decisions:

1. FX11 must not block installation merely because the hardware does not satisfy Microsoft's stock Windows 11 compatibility gate.
2. FX11 should provide its own GRUB-based boot manager for multi-OS systems, with FX11 visual branding.

## 1. Installation compatibility policy

FX11 Installer is not the stock Windows Setup compatibility experience.

The normal FX11 deployment path should apply the selected Windows image directly to the prepared FX11 partition from the FX11 installation environment, then configure boot files, WinRE and OOBE. Because FX11 controls deployment, the stock Windows Setup hardware compatibility screen is not the authority that decides whether installation may continue.

FX11 should therefore not stop installation solely because of stock Windows 11 checks such as:

- unsupported CPU generation/model,
- missing or unsupported TPM version,
- Secure Boot not enabled,
- low RAM relative to Microsoft's normal Windows 11 gate,
- other Microsoft Setup compatibility blocks that are not technically required for the FX11 deployment engine itself to copy and boot the selected image.

### FX11 rule

**Warn, explain, allow. Do not silently block where deployment is technically possible.**

The installer may show compatibility information such as:

- CPU outside Microsoft's supported Windows 11 list,
- TPM missing or below the Microsoft-recommended level,
- Secure Boot disabled,
- RAM/storage below FX11's recommended level,
- missing virtualization/security capabilities.

These are advisory unless a capability is actually required by the selected FX11 installation path.

Examples of genuine blockers may include:

- the firmware/boot mode is incompatible with the selected layout,
- the target disk cannot be accessed,
- the target partition is too small to hold the selected Windows image,
- the selected image cannot be applied or boot files cannot be installed,
- the CPU architecture does not match the Windows image.

FX11 should not claim unsupported hardware is guaranteed to receive every future Windows update or driver. The compatibility screen should distinguish between:

- **Microsoft Windows 11 supported hardware**,
- **FX11 installation technically possible**,
- **FX11 recommendation/warning**.

This follows the project principle: **FX11 recommends; the user decides.**

## 2. Deployment method

The preferred implementation is to avoid launching `setup.exe` for the actual installation path.

FX11 Installer should instead perform image deployment directly:

1. FX Partition Manager prepares the selected disk layout.
2. FX11 Installer reads the handoff manifest.
3. The selected Windows image is applied directly to the FX11 NTFS target.
4. UEFI boot files are installed to the selected EFI System Partition.
5. WinRE is deployed and registered when Recovery is selected.
6. OOBE is prepared for the first normal Windows boot.

This architecture is more robust than depending on version-specific registry tricks intended only to persuade stock Windows Setup to ignore its own compatibility checks.

Compatibility bypass registry values may still be supported as a fallback path if FX11 ever launches Microsoft Setup for a special case, but they are not the primary design.

## 3. FX Boot Manager

FX11 should provide a GRUB-based boot manager presented to the user as **FX Boot Manager**.

Its job is to present available operating systems cleanly after firmware startup and allow the user to choose what to boot.

Typical entries may include:

- **FX11**,
- an existing Windows installation or Windows Boot Manager,
- Linux installations,
- BSD installations,
- other UEFI boot loaders that can be safely chainloaded.

### Detection model

FX Boot Manager must not invent operating systems from names alone.

Detection should use evidence available from:

- UEFI NVRAM boot entries,
- EFI executables present on detected EFI System Partitions,
- partitions detected by FX Partition Manager,
- existing bootloader metadata where readable,
- GRUB/os-prober style discovery where technically available and safe.

When detection is uncertain, the UI should identify the entry by loader/path rather than falsely naming an operating system.

Existing boot loaders should be preserved whenever possible.

### FX11 entry

The FX11 entry should normally chainload the Microsoft Windows boot loader installed for the FX11 installation rather than replace Windows' own BCD logic internally.

Conceptually:

`FX Boot Manager (GRUB) -> FX11 entry -> Windows Boot Manager -> FX11`

This keeps Windows servicing and recovery behavior closer to standard expectations while giving the user an FX-branded top-level multi-OS menu.

### Existing systems

Where an existing Linux/BSD/other UEFI loader is detected, FX Boot Manager may chainload that loader directly.

The installer must not delete an existing boot entry merely because FX Boot Manager becomes first in UEFI boot order.

The user should be able to restore another boot manager as the firmware default later.

## 4. Secure Boot

GRUB introduces an important compatibility consideration: Secure Boot.

FX11 must not pretend that an arbitrary unsigned GRUB binary will boot with Secure Boot enabled.

### Current development target

For the first working FX11 release and today's implementation target, **Secure Boot is intentionally disabled**.

The installer should detect the Secure Boot state and show a clear message before installing FX Boot Manager:

> FX Boot Manager in this build requires Secure Boot to be disabled. FX11 does not change firmware settings automatically.

If Secure Boot is enabled, the installer must not silently install an unsigned GRUB path and leave the machine unbootable. It should stop the FX Boot Manager installation step and offer one of these choices where available:

- reboot to firmware settings so the user can disable Secure Boot,
- continue with Windows Boot Manager only,
- cancel and return to the installation summary.

Secure Boot being disabled must not prevent the FX11 operating system itself from being installed if the selected deployment path is otherwise valid.

### Production target

The planned production design is a Secure Boot compatible FX Boot Manager chain:

`UEFI Secure Boot -> trusted shim -> signed FX GRUB -> selected operating system loader`

The intended implementation should support:

- a trusted/signed shim suitable for Secure Boot,
- FX GRUB signed by a key trusted by that shim,
- preservation of the Microsoft Windows boot loader as the FX11 chainload target,
- validation of every executable component in the Secure Boot chain,
- key rotation and revocation planning,
- support for current Microsoft UEFI CA trust requirements where applicable.

Until that signed production chain is available and tested, FX11 must describe Secure Boot support as planned rather than imply that the current unsigned GRUB build supports it.

### Explicit supported states

FX11 therefore recognizes these states:

- **Current development mode: Secure Boot OFF + FX Boot Manager**,
- **Fallback: Secure Boot ON + Windows Boot Manager only**,
- **Future production mode: Secure Boot ON + signed FX Boot Manager chain**.

FX11 should never silently disable Secure Boot in firmware.

## 5. Visual design

FX Boot Manager should be themed to match FX11.

Theme requirements:

- FX11 wallpaper/background,
- FX branding,
- large readable OS names,
- clear selected-entry highlight,
- countdown visible but not intrusive,
- keyboard navigation,
- sensible display scaling where GRUB supports it,
- fallback text mode if graphics fail.

The default entry after a fresh installation is **FX11**, but the user can change it later in FX11 Control Center.

Suggested default timeout: 5 seconds, configurable later.

For the first build, the theme should be kept separate from GRUB logic so the background, logo and menu styling can later be replaced without changing boot detection or chainloading code.

## 6. Multi-OS safety

The installer should distinguish between:

- installing FX Boot Manager,
- preserving detected EFI loaders,
- changing UEFI boot order.

These are separate actions.

Before applying boot changes, the final review should show:

- ESP that will receive FX Boot Manager,
- FX11 Windows boot-loader path,
- detected existing boot entries,
- entries that will be added to the FX Boot Manager menu,
- whether firmware boot order will change,
- Secure Boot compatibility state.

No existing OS partition should be modified solely because a boot menu entry is being added.

## 7. Recovery and escape hatch

FX11 installation media should include boot repair capabilities.

At minimum the repair path should be able to:

- reinstall FX Boot Manager,
- regenerate the GRUB menu from detected loaders,
- restore/reinstall the Windows Boot Manager entry for FX11,
- set Windows Boot Manager or another detected loader as firmware default,
- show current UEFI boot entries and ESP contents before changing them.

This prevents FX Boot Manager from becoming a single point of failure.

## 8. Implementation order

For the first working installer, implementation should proceed in this order:

1. UEFI/GPT only.
2. Secure Boot detection and explicit status in the installer.
3. Unsigned GRUB-based FX Boot Manager for Secure Boot OFF.
4. Preserve existing EFI loaders and UEFI boot entries.
5. Create a dedicated FX11 menu entry that chainloads Windows Boot Manager.
6. Detect other UEFI loaders and expose them without modifying their partitions.
7. Add the FX11 visual theme/background.
8. Add boot repair from FX11 installation media.
9. Add signed shim/GRUB development and Secure Boot validation in QEMU/OVMF.
10. Move to production Secure Boot signing only after the full chain has been audited and tested.

## Product summary

The current development model is:

`UEFI + Secure Boot OFF -> FX Boot Manager -> chosen OS`

and for FX11 specifically:

`UEFI -> FX Boot Manager -> Windows Boot Manager -> FX11`

The future production model is:

`UEFI + Secure Boot ON -> trusted shim -> signed FX Boot Manager -> chosen OS`

FX11 compatibility policy is equally simple:

**Microsoft support status is shown as information; FX11 installation is blocked only by a real technical requirement of the selected deployment path.**
