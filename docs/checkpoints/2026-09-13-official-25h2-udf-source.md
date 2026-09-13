# Checkpoint — official Windows 11 25H2 UDF source compatibility

Date: 2026-09-13

## Observed real source

The first genuine Windows 11 source used for FX11 is:

- local filename: `Win11_25H2_Polish_x64_v2.iso`
- volume id reported by xorriso: `CCCOMA_X64FRE_PL-PL_DV9`
- SHA-256: `9453d410298e50c36ce31153326857848256e0980ff8fda501b4d3817540beb9`
- size reported externally / by Microsoft metadata: about 7.77 GB

The SHA-256 matches Microsoft's published checksum for the current Polish Windows 11 25H2 x64 v2 image. The source is therefore treated as genuine/expected, not corrupted.

## Failure observed

`fx11 inspect` and consequently `fx11 build` fail with:

`No /sources/install.wim or /sources/install.esd found in the ISO.`

The xorriso log for this real Microsoft image shows only the ISO9660 root (`1 nodes read`) and reports a hidden EFI El Torito image. This differs from the synthetic ISO used by the test harness, whose file tree is directly visible to xorriso.

## Diagnosis

This is an FX11 Builder source-media compatibility gap, not a bad Windows ISO.

Current Builder assumptions are too narrow:

1. `src/fx11/iso.py` extracts `/sources/install.wim` or `/sources/install.esd` only through xorriso's ISO9660 view.
2. `src/fx11/winpe.py` extracts `/sources/boot.wim` the same way.
3. `src/fx11/builder.py` rebuilds by opening the source through xorriso and replaying its visible ISO tree / boot metadata.
4. `src/fx11/media_efi.py` currently requires a file-backed EFI El Torito image path and rejects interval/appended/hidden EFI layouts.

Current Microsoft media can expose the Windows file tree through UDF while xorriso does not expose it as a normal ISO9660 tree. FX11 must support this directly; users should not be told to find an older or repacked Windows image merely to fit the Builder.

## Direction

Add a real-Microsoft-media path that:

- detects when the source tree is not usable through xorriso,
- uses a non-root UDF-capable reader/extractor (initial candidate: 7-Zip / `7z`) for Windows files,
- extracts `install.wim`/`install.esd` and `boot.wim` through a common source-media abstraction,
- reconstructs the FX11 output ISO from the extracted Microsoft tree instead of assuming xorriso can replay the UDF source tree,
- reconstructs BIOS/UEFI El Torito boot entries explicitly when the source EFI image is hidden/interval-backed,
- preserves the source ISO and records its exact SHA-256 in the manifest,
- validates the rebuilt image in QEMU/OVMF before real-hardware use.

Synthetic ISO tests remain useful but are no longer sufficient to claim compatibility with current Microsoft download media.

## Status

Blocked before real ISO build at source-media inspection. GParted input remains verified and unrelated to this failure.
