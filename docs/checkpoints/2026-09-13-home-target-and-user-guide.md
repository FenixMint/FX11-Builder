# Checkpoint — Windows 11 Home target and Builder user guide

Date: 2026-09-13

## Real Microsoft UDF inspection passed

The user ran `fx11 inspect` against the real source image:

- `Win11_25H2_Polish_x64_v2.iso`
- SHA-256 `9453d410298e50c36ce31153326857848256e0980ff8fda501b4d3817540beb9`
- source media successfully read through the new UDF-capable path
- install image format: WIM

Observed editions:

1. Windows 11 Home `[Core]`
2. Windows 11 Home N `[CoreN]`
3. Windows 11 Education `[Education]`
4. Windows 11 Education N `[EducationN]`
5. Windows 11 Pro `[Professional]`
6. Windows 11 Pro N `[ProfessionalN]`
7. Windows 11 Pro Education `[ProfessionalEducation]`
8. Windows 11 Pro Education N `[ProfessionalEducationN]`
9. Windows 11 Pro for Workstations `[ProfessionalWorkstation]`
10. Windows 11 Pro N for Workstations `[ProfessionalWorkstationN]`

The inspection completed successfully on Linux Mint 22.3 with `fx11 doctor` reporting READY and the 7-Zip UDF reader present.

## Current real-build target

The user's current Windows entitlement is for Windows 11 Home, therefore the first genuine FX11 build should explicitly target:

```text
--edition "Windows 11 Home"
```

Use the edition name rather than relying on index `1`, because image indexes can differ between Microsoft source ISOs.

This is not a licensing bypass. FX11 Builder does not provide Windows licenses or activation keys and should build the edition that matches the user's legitimate entitlement.

## User guide

A plain-text operating guide was added at the repository root:

```text
FX11_BUILDER_INSTRUKCJA.txt
```

The guide covers:

- Debian / LMDE / Linux Mint bootstrap,
- updating the Builder,
- `fx11 doctor`,
- source ISO inspection,
- GParted verification,
- profiles and dry-run,
- a Windows 11 Home build example,
- validation and audit,
- QEMU/OVMF testing,
- WinPE fallback,
- Secure Boot development limitation,
- common errors,
- repository documentation map,
- the principle that observed tests are required before claiming a feature works.

The guide is intended to be maintained with the Builder as commands and support status evolve.
