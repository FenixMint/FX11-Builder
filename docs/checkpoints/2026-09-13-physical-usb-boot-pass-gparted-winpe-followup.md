# 2026-09-13 — first physical hybrid USB boot succeeds; GParted/WinPE follow-up

## Observed on physical hardware

The GPT/EFI hybrid FX11 ISO was written to a Kingston DataTraveler 3.0 and the machine successfully booted the FX11 UEFI path from USB.

This is the first observed physical-hardware confirmation of:

- firmware recognizing the hybrid FX11 USB,
- FX11 UEFI boot taking control from physical removable media.

## GParted issue observed

The GParted Live path still presented technical startup questions including display resolution, color depth and graphics-driver/X configuration. A manual ATI choice was attempted and the GParted startup then hung.

Product requirement confirmed: the normal FX Partition Manager path must not expose those technical GParted Live/X configuration questions. It should boot directly into the graphical GParted environment. At most a language choice may remain in the eventual UX.

Immediate development change:

- add GParted Live `gl_batch` boot parameter,
- preselect locale and keyboard for the current Polish development build (`pl_PL.UTF-8`, `pl`),
- rely on GParted/Debian automatic graphics detection rather than asking the user to select a graphics driver, resolution or color depth.

The upstream GParted Live boot-parameter documentation defines `gl_batch` specifically for suppressing X configuration questions during boot.

## FX11 Installer / WinPE issue observed

The `FX11 Installer / WinPE fallback` GRUB entry produced an error and did not start WinPE on the physical USB test.

The previous entry chainloaded the preserved `/efi/microsoft/boot/bootmgfw.efi` copy. The next diagnostic build changes the primary Microsoft handoff to `/bootmgr.efi`, matching the Microsoft optical-media boot-manager path present in the Windows installation tree.

This change is diagnostic until observed on physical hardware. If it still fails, capture the exact GRUB/EFI error text and continue from that evidence rather than guessing.

## Fast retest path

`scripts/repack-fx11-usb-hybrid.sh` now refreshes `/FX11/media/grub.cfg` from the current checkout before rebuilding the hybrid ISO. This lets the GParted and WinPE menu fixes be tested without repeating the expensive WIM export/customization stage.

## Status

Confirmed:

- hybrid USB physical boot: PASS.

Pending physical retest:

- GParted should reach its GUI without graphics/keymap/language/X prompts,
- WinPE fallback should start through `/bootmgr.efi`,
- exact WinPE failure text is still needed if the revised handoff does not work.
