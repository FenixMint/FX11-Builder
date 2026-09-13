# Checkpoint — synthetic FX11 E2E PASS

Date: 2026-09-13

This checkpoint records the first fully observed synthetic end-to-end FX11 Builder pass on the current Linux-host toolchain before moving to a genuine Microsoft Windows 11 source ISO.

## Linux Mint local result

User host:

- Linux Mint 22.3
- x86_64
- kernel 7.0.0-31-generic

On commit `de88466fa673fc1a92bb190ff69e859dd8b30e95`, the user ran:

```bash
PATH="$PWD/.venv/bin:$PATH" tests/e2e_synthetic.sh
```

Observed final result:

```text
FX11 synthetic end-to-end build with partition-to-installer handoff: PASS
EXIT CODE: 0
```

The observed run successfully:

- created a synthetic multi-edition Windows-style source ISO,
- inspected Home and Pro image indexes,
- selected Windows 11 Pro,
- produced the current FX11 build plan (`tiny11-safe`, `privacy-balanced`),
- exported a single-image `install.wim`,
- customized and verified `boot.wim`,
- staged SetupComplete, FX11 PowerShell provisioning, manifest, and FX boot-manager payload,
- rebuilt the ISO,
- validated the generated output ISO,
- verified the partition-manager-to-installer WinPE handoff assertions,
- exited with code 0.

The xorriso warning about no `/EFI/BOOT` directory in the synthetic source/build remains visible and must not be confused with a runtime failure. The dedicated FX UEFI/GParted path is tested separately; a genuine Windows ISO + GParted + QEMU/OVMF boot test is the next validation checkpoint.

## Debian 13 CI result

GitHub Actions run `34767229234` for the same commit completed successfully.

The `debian:trixie` job therefore confirms on Debian 13:

- dependency installation,
- Python virtual environment and editable package install,
- all current unit tests,
- `fx11 doctor` READY,
- synthetic end-to-end build and validation harness.

This is strong evidence that Debian 13 is a working FX11 Builder host for the current synthetic pipeline. Full host validation still requires a genuine Microsoft Windows 11 ISO build and normal output validation on that host.

## Next checkpoint

Use a genuine Microsoft Windows 11 ISO together with the already SHA-256-verified pinned GParted Live 1.8.1-6 image, then:

1. `fx11 inspect` the real source ISO,
2. build one selected edition with `--gparted-live`,
3. `fx11 validate` the resulting ISO,
4. boot the ISO in QEMU/OVMF,
5. confirm the expected FX GRUB -> FX Partition Manager (GParted) path and WinPE fallback,
6. only then move to destructive real-hardware installation testing.
