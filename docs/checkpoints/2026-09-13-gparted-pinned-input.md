# Checkpoint — pinned GParted Live input

Date: 2026-09-13

FX11 mainline partitioning uses the GParted-based graphical path, while the native FX text partition manager remains fallback/recovery and an independent development path.

## Pinned upstream input

The first pinned GParted Live build input is:

- GParted Live: `1.8.1-6`
- GParted application: `1.8.1`
- architecture: `amd64`
- Linux kernel: `7.1.12-1`
- file: `gparted-live-1.8.1-6-amd64.iso`
- SHA-256: `d789c38779f0d6f7026c12f44c2c52a04f66e28a1aea7d51f3045ad1bbf28411`
- upstream release page: `https://sourceforge.net/projects/gparted/files/gparted-live-stable/1.8.1-6/`
- project: `https://gparted.org/`

This was cross-checked against the upstream GParted release announcement and SourceForge release metadata.

## Supply-chain rule

FX11 Builder must reject a GParted Live image whose SHA-256 does not exactly match the pinned release. No `latest` alias or mutable third-party binary may silently enter a release build.

Implemented files:

- `third_party/gparted-live-1.8.1-6.json`
- `src/fx11/gparted.py`
- `tests/test_gparted.py`

The verifier is intentionally local-only at this stage: a build input is supplied explicitly and verified before future import into the combined FX11 installation image. Automatic downloading is not yet part of the trusted build path.

## Next implementation step

Extract the minimum bootable GParted Live payload into an FX-owned path in the generated installation media, then add a top-level boot path that can start FX Partition Manager before WinPE while preserving the existing WinPE/text fallback.
