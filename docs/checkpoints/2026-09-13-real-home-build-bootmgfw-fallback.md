# Checkpoint — 2026-09-13 — first real Windows 11 Home build fallback failure

## Observed on real Microsoft Windows 11 25H2 Polish x64 media

Source:
- `/home/hype/Pobrane/Win11_25H2_Polish_x64_v2.iso`
- SHA-256: `9453d410298e50c36ce31153326857848256e0980ff8fda501b4d3817540beb9`
- source media detected as UDF
- selected edition: `Windows 11 Home`, source image index 1
- GParted Live input had already verified against the pinned SHA-256

The real build progressed through the expensive parts successfully:
- selected Home image export completed
- generated single-image `install.wim` reached 6438 MiB integrity-table verification
- customized WinPE `boot.wim` verified successfully

The build then stopped before ISO creation with:

`ERROR: Microsoft bootmgfw.efi is missing from the UDF source; cannot keep the WinPE fallback while FX GRUB owns /efi/boot/bootx64.efi.`

No FX11 output ISO was produced, so subsequent `validate`, `audit`, and `test` correctly failed with `ISO not found` / `Output ISO is missing`.

## Root cause

The UDF repack path assumed `/efi/microsoft/boot/bootmgfw.efi` was exposed as a normal file in the Microsoft UDF tree. The tested 25H2 source does not expose that file there, but it does expose the signed removable-media Windows loader at `/efi/boot/bootx64.efi`.

FX11 currently wants both:
- the removable-media path `/efi/boot/bootx64.efi` to contain FX GRUB, for filesystem/removable-media fallback,
- a separate Microsoft UEFI loader path for the explicit WinPE fallback entry.

## Implemented fix

`src/fx11/iso.py` now provides `ensure_windows_uefi_fallback(media_tree)`.

During extraction of UDF Microsoft media:
1. if `/efi/microsoft/boot/bootmgfw.efi` already exists, it is retained unchanged;
2. otherwise the original Microsoft `/efi/boot/bootx64.efi` is copied byte-for-byte to `/efi/microsoft/boot/bootmgfw.efi`;
3. the copy is SHA-256 checked against the original before the build continues;
4. only after that preservation step may the Builder replace `/efi/boot/bootx64.efi` with the FX GRUB loader.

This keeps an original Microsoft-signed loader available for the WinPE fallback without modifying its contents. The resulting chainload behavior still requires OVMF/QEMU validation.

Tests were added for:
- preserving an existing `bootmgfw.efi`,
- creating the fallback from `bootx64.efi`,
- byte/SHA equality of the preserved copy,
- rejecting media with neither Microsoft UEFI loader path.

Implementation commits:
- `c92432fdcaf6d428269c4872afce4667f79c543e` — preserve Windows UEFI fallback on UDF media
- `b37ee7107290a20a0f5ad970560881c8556e69c1` — unit tests for fallback preservation

## Superseded implementation idea

An earlier note in this checkpoint proposed leaving Microsoft's `/efi/boot/bootx64.efi` in place and using FX GRUB only through the El Torito image. That remains a possible ISO-only architecture, but it is **not the implementation currently committed**. The current implementation preserves the Microsoft loader by copying it to the canonical Microsoft boot-manager path, then lets FX GRUB own the removable-media path. This also keeps the door open for later USB media support.

## Status

- Real Home build attempt #1: **FAILED at UEFI fallback staging**
- WIM export/integrity stage: **observed working**
- WinPE customization: **observed working**
- fallback preservation fix: **implemented, not yet validated on the real source build**
- ISO generation: **not yet observed on the real source**
- QEMU/OVMF boot: **not reached**

Do not claim the real 25H2 Home ISO build works until the corrected build completes and the resulting ISO passes validation and OVMF/QEMU boot tests.
