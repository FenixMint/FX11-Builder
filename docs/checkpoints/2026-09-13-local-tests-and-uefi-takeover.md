# Checkpoint — local tests green and FX UEFI media takeover

Date: 2026-09-13

## Local validation reported by user

After pulling main at commit `38cf18d2c2249ce6d16ad46547592cda2b30289a`, the reference Linux host completed:

- `python -m compileall -q src`
- `fx11 gparted info`
- `pytest tests/test_gparted.py tests/test_media_boot.py`
- full `pytest`

Results reported:

- GParted/media tests: **8 passed**
- full test suite: **53 passed**

This is a local Linux validation checkpoint, not a claim that the real Windows installation path or GitHub CI has completed.

## Next implementation started immediately after the checkpoint

The GParted mainline build now gains an FX-controlled UEFI El Torito image.

Design:

`UEFI -> FX GRUB -> FX Partition Manager (GParted default) / FX11 WinPE fallback`

Key points:

- only builds with `--gparted-live` replace the source file-backed UEFI El Torito image,
- builds without GParted keep the previous Microsoft-media boot path,
- source BIOS boot metadata remains source-derived through xorriso replay,
- FX creates a small FAT image containing unsigned `EFI/BOOT/BOOTX64.EFI`,
- that EFI binary is a GRUB standalone image with an embedded handoff to `/FX11/media/grub.cfg`,
- `/FX11/media/grub.cfg` defaults to `FX Partition Manager — powered by GParted`,
- WinPE remains an explicit fallback entry,
- Secure Boot remains OFF for the current unsigned development chain,
- the generated EFI image is also stored under `/FX11/media/efiboot.img` for provenance/audit,
- output validation checks that the source file-backed EFI El Torito path was actually replaced by the expected FX image hash.

## New dependency

`mtools` is used to create the FAT EFI El Torito image without requiring privileged loop mounts.

Debian/Mint bootstrap and Debian CI smoke environment now install `mtools`.

## Relevant commits after the 53-test checkpoint

- `413f6cf9f7dc3de29a605893842dac940d266d3d` — Build FX11 UEFI El Torito boot image
- `ae1cd520e758a3f1a55d55744c743317b3a4d344` — Test FX11 UEFI El Torito boot image planning
- `a6faf7d47479868ebf258902a46dac6bebc1904e` — Make FX GRUB the UEFI media entry for GParted builds
- `468de1afdb4c4daaf2c59a3407fa5a1d7d67f368` — Install mtools for FX11 UEFI media image
- `4b98ce7eb6ab52f0c23c5000aff498f168d51759` — Install mtools in Debian smoke environment
- `73db67463f0f68e54993e8a85ee1790adc013b57` — Report GRUB as required and mtools for GParted media
- `baba4156d346e87da833ff3454e61e258226dfa8` — Smoke-test generated FX11 media EFI image

## Validation status

At the time of this checkpoint:

- the previous local suite is green at 53 tests,
- the new UEFI takeover commits still require a fresh local pull/test on the user's machine,
- GitHub combined status had not yet reported checks for the latest commit,
- a genuine Microsoft Windows 11 ISO + pinned GParted Live build and QEMU/OVMF boot remain the next decisive validation.
