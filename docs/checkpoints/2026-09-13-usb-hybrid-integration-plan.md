# FX11 USB-hybrid integration plan — 2026-09-13

## Decision

The one-off hybrid repack is a diagnostic step only. If the repacked ISO boots correctly from physical USB, the fix must be integrated into FX11 Builder itself and committed to the public GitHub repository.

## Target state

A normal `fx11 build` should directly produce an ISO that preserves the existing optical/QEMU boot path while also being suitable for raw USB writing.

Required characteristics:

- existing BIOS El Torito boot remains available;
- existing FX GRUB UEFI El Torito boot remains available;
- the output ISO contains a valid System Area / partition layout for USB boot;
- the existing EFI boot image is exposed as an EFI System Partition where appropriate;
- `fx11 validate` should detect and reject a build that lacks the expected USB-hybrid structure once this becomes the supported output format;
- tests must cover the generated xorriso arguments / structural validation;
- documentation must state that one FX11 ISO is intended for DVD/ISO use and direct USB imaging.

## Validation gate

Do not call the Builder fixed until the diagnostic hybrid ISO is observed booting from a real USB device on physical hardware. After that observation, fold the change into `src/fx11/builder.py`, add tests, update docs/history, run pytest/CI, and then treat the GitHub version as the corrected Builder.

Microsoft Windows binaries / generated FX11 ISO are not to be committed to the repository; only Builder code, tests and documentation are committed.
