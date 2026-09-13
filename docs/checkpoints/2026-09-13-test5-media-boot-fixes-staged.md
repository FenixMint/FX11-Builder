# Test5 media boot fixes staged — 2026-09-13

This checkpoint follows the physical finding that GParted automatic graphics worked, while the graphical FX11 GRUB theme did not render and the `FX11 Installer` entry failed with `Error: cannot load image.`

## Changes staged for the next physical iteration

- WinPE chainload target restored from the failed direct `/bootmgr.efi` experiment to the preserved Microsoft removable-media EFI loader at `/efi/microsoft/boot/bootmgfw.efi`.
- The fast hybrid repack now rebuilds the FX11 media `BOOTX64.EFI` from the current checkout instead of retaining the older EFI binary from the base test ISO.
- The FX11 theme is copied into the writable `FX11BOOT` FAT EFI image under `/EFI/FX11/theme/` in addition to the ISO-tree copy.
- Media GRUB prefers the EFI-resident font/theme/background and also calls `background_image` directly before applying the richer theme. This creates a visible background fallback if theme parsing is incomplete on real firmware.
- Required graphical GRUB modules are explicitly requested when building the standalone UEFI binary.
- Added a GParted Live boot-time handoff hook. The nested GParted ISO receives `/live/config-hooks/90-fx11-continue`, and GParted boots with `hooks=medium`.
- The hook adds `Continue to FX11 Installer` as an application/desktop launcher. It writes `/EFI/FX11/continue-installer` to the `FX11BOOT` FAT partition and reboots.
- Media GRUB detects that marker and preselects `FX11 Installer` on the next boot with a 3 second timeout.

## Validation status

These are code changes for the next test image. They are not yet a physical pass. In particular, the following still require observation on real hardware:

1. EFI-resident graphical theme/background rendering;
2. preserved Microsoft EFI loader successfully entering WinPE;
3. GParted live-config medium hook creating the launcher;
4. launcher writing the marker and rebooting;
5. GRUB honoring the marker and selecting the installer.

The marker is intentionally still a development mechanism. Automatic marker removal by WinPE should be added once the WinPE entry itself is confirmed to boot reliably.
