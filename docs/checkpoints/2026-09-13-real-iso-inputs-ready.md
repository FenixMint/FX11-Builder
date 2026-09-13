# Checkpoint — ready for first genuine FX11 ISO build

Date: 2026-09-13

This checkpoint records the local state immediately before building the first FX11 ISO from a genuine Microsoft Windows 11 source image.

## Confirmed locally on Linux Mint 22.3

Repository state after pulling through `c75d64b`:

- `pytest tests/test_vm.py`: **1 passed**
- full `pytest`: **60 passed**
- earlier synthetic end-to-end harness: **PASS**
- synthetic E2E exit code: **0**

The synthetic E2E successfully exercised edition selection, single-image WIM export, WinPE payload injection, provisioning file staging, ISO rebuild, structural validation, and partition-manager-to-installer handoff assertions.

## Genuine build inputs discovered locally

Windows source ISO:

- `/home/hype/Pobrane/Win11_25H2_Polish_x64_v2.iso`

Pinned graphical partition-manager input:

- `/home/hype/Pobrane/FX11/gparted-live-1.8.1-6-amd64.iso`
- previously verified SHA-256: `d789c38779f0d6f7026c12f44c2c52a04f66e28a1aea7d51f3045ad1bbf28411`

## Next validation sequence

1. Run `fx11 inspect` against the genuine Microsoft ISO and confirm the desired edition/index.
2. Re-verify the pinned GParted Live ISO.
3. Build the first genuine FX11 ISO with GParted enabled.
4. Run `fx11 validate`.
5. Run `fx11 audit` against the original source ISO.
6. Boot the generated ISO in QEMU/OVMF before any destructive real-hardware installation.

Do not claim successful real Windows deployment, GParted boot, WinPE fallback boot, OOBE provisioning, or real-hardware installation until each is observed directly.
