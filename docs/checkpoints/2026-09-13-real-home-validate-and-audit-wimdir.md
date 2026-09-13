# Checkpoint — 2026-09-13 — real Home validation + audit wimdir fix

## Real FX11 Home ISO validation

Validated local artifact:

- `/home/hype/Pobrane/FX11/FX11-25H2-PL-x64-Home-test2.iso`
- `fx11 validate` result: `VALID`
- SHA-256: `4cb0b97e396441f6271c659a51245d89d8e6caaa0844f400edb90d04dc2936cd`
- checksum file contained the same SHA-256
- volume ID: `FX11`
- El Torito BIOS image: `/boot/etfsboot.com`
- El Torito UEFI image: `/efi/microsoft/boot/efisys.bin`
- UEFI El Torito load size: 16 MiB (`32768` x 512-byte sectors)
- ISO tree: 1191 nodes reported by xorriso
- media size: 4,110,460 sectors / about 8,028 MiB

This confirms the real rebuilt 25H2 Home ISO survives the Builder's output validation and contains explicit BIOS + UEFI El Torito boot entries. It does **not** yet prove that FX GRUB, GParted, or the WinPE fallback boot correctly in OVMF/QEMU; those remain the next runtime checkpoint.

## Audit failure observed

Command:

```bash
fx11 audit "$WINISO" "$OUT" -o "$OUT.delta.json"
```

failed with:

```text
ERROR: Unable to inventory WIM image 1: ERROR: Too many arguments
Usage:
    wimlib-imagex dir WIMFILE [IMAGE] [--path=PATH] [--detailed]
```

Root cause was in `src/fx11/audit.py`: `list_wim_files()` invoked:

```text
wimlib-imagex dir WIMFILE IMAGE /
```

The bare `/` is not a supported positional path argument in current wimlib. `wimdir` already lists recursively from the root by default; an alternate subtree would use `--path=PATH`.

## Fix implemented

`list_wim_files()` now invokes:

```text
wimlib-imagex dir WIMFILE IMAGE
```

and parses each complete absolute output line rather than `line.split()[-1]`, preserving Windows paths containing spaces such as `/Program Files/...`.

Regression coverage was added to assert both the exact supported command shape and path-with-spaces parsing.

## Status

- real Windows 11 25H2 Home build: **PASS / BUILD VALID**
- real output `fx11 validate`: **PASS / VALID**
- El Torito structural inspection: **PASS, BIOS + UEFI entries present**
- real `fx11 audit`: **FAILED before fix; rerun required**
- OVMF/QEMU FX GRUB boot: **not yet tested**
- GParted nested boot: **not yet tested**
- WinPE fallback boot: **not yet tested**

Do not mark the real audit or boot chain as passed until observed on the corrected code.
