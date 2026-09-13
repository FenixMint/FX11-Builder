# Checkpoint — 2026-09-13 — first successful real Windows 11 Home FX11 build

## Observed local host

Host: Linux Mint 22.3, x86_64.

Source Windows ISO:
- `/home/hype/Pobrane/Win11_25H2_Polish_x64_v2.iso`
- SHA-256: `9453d410298e50c36ce31153326857848256e0980ff8fda501b4d3817540beb9`
- detected as UDF
- selected edition: `Windows 11 Home`, source image index 1

Pinned GParted Live input:
- version `1.8.1-6`
- SHA-256 `d789c38779f0d6f7026c12f44c2c52a04f66e28a1aea7d51f3045ad1bbf28411`

## Tests before build

Observed locally immediately before the build:
- `pytest tests/test_iso.py` -> `10 passed in 0.09s`
- full `pytest` -> `66 passed in 0.63s`

The corresponding GitHub Actions run for commit `b39c9da01b9d8062567a953d494cd4c710f34800` later completed successfully for both:
- `unit`
- `debian-smoke` including dependency install, full pytest, `fx11 doctor`, and synthetic E2E

## Real build result

Output:
- `/home/hype/Pobrane/FX11/FX11-25H2-PL-x64-Home-test2.iso`
- reported size by `ls -lh`: about `7.9G`
- SHA-256: `4cb0b97e396441f6271c659a51245d89d8e6caaa0844f400edb90d04dc2936cd`
- checksum file: `/home/hype/Pobrane/FX11/FX11-25H2-PL-x64-Home-test2.iso.sha256`

Observed builder result:
- `BUILD VALID`
- edition: `Windows 11 Home`
- profiles: `tiny11-safe, privacy-balanced`
- GParted Live staged: `1.8.1-6`
- build exit code: `0`
- elapsed time: `10m28.808s`

xorriso completed the repacked media write successfully:
- `ISO image produced: 4110460 sectors`
- `Written to medium : 4110460 sectors at LBA 0`
- El Torito metadata was detected when the completed `.building` image was reopened

## What this proves

This is the first observed successful build of a real Microsoft Windows 11 25H2 Polish x64 source into an FX11 Windows 11 Home ISO using the UDF-source path and the pinned GParted payload.

It proves the builder can complete the real-media extraction/export/customization/repack pipeline on the tested Linux Mint host and produce an internally validated ISO artifact.

## What is not yet proven

Do not yet call this a fully validated install image or host-support milestone. Still required:
- standalone `fx11 validate` on the final output path
- deep `fx11 audit` against the original UDF source
- QEMU/OVMF boot of FX GRUB
- boot of GParted Live from the staged nested ISO
- WinPE fallback boot
- full installation to a disposable virtual disk
- OOBE / post-install provisioning verification
- later real-hardware validation

## Status

Real Windows 11 Home build: **SUCCESS**.
Boot/runtime validation: **pending**.
