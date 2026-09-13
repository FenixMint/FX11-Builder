# Checkpoint — Mint local pass and Debian 13 smoke status

Date: 2026-09-13

## Local Linux Mint validation

Host observed by the user:

- Linux Mint 22.3
- x86_64
- kernel 7.0.0-31-generic

At repository state `ab091a0` the user observed:

- focused UEFI/GParted tests: **14 passed**
- full unit suite: **59 passed**
- `fx11 doctor`: **READY**
- `wimlib-imagex`: OK
- `xorriso`: OK
- `grub-mkstandalone`: OK
- `mformat` / mtools: OK
- QEMU: OK

Pinned GParted Live input remains verified locally:

- `gparted-live-1.8.1-6-amd64.iso`
- SHA-256 `d789c38779f0d6f7026c12f44c2c52a04f66e28a1aea7d51f3045ad1bbf28411`

The earlier local git conflict was only the executable-bit change on `scripts/bootstrap-debian.sh`; no source-code modification was lost.

## Debian target status

FX11 Builder explicitly targets Debian-family hosts. GitHub Actions currently runs `debian:trixie` as the Debian smoke environment.

For commit `ab091a0`, Debian 13 / trixie successfully completed:

- dependency installation,
- Python virtual environment creation,
- editable FX11 Builder installation,
- all **59 unit tests**,
- `fx11 doctor` with **STATUS: READY**.

The Debian job then failed only in the synthetic E2E shell harness because the test addressed an extracted WinPE filename using exact Linux filename casing. Windows/WIM paths are case-insensitive, while Debian's filesystem is case-sensitive. This is a test-harness portability issue, not evidence that the builder dependencies or Python code fail on Debian.

The synthetic E2E check is being hardened to resolve extracted WinPE payload filenames case-insensitively while still failing if any required payload file is actually absent.

## Support wording

Current wording should remain precise:

- Linux Mint 22.3: locally validated unit/tooling checkpoint.
- Debian 13 / trixie: CI dependency/unit/doctor checkpoint validated; synthetic E2E harness fix pending confirmation.
- LMDE: intended Debian-family target, but do not claim a full genuine-Windows-ISO build until actually tested.

A distribution becomes fully validated for FX11 Builder only after a genuine Microsoft Windows ISO build and normal FX11 validation path succeed on that host.
