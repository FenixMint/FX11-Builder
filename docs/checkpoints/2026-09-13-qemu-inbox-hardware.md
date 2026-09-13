# Checkpoint — Windows-compatible QEMU hardware baseline

Date: 2026-09-13

Before the first genuine FX11 ISO boot test, the QEMU baseline was changed to avoid depending on third-party VirtIO drivers that are not present in stock Windows/WinPE media.

## Decision

The default `fx11 test` VM should exercise FX11 itself, not fail because Windows Setup cannot see a VirtIO disk or network adapter.

The baseline VM therefore uses emulated devices intended to work with inbox Windows/WinPE support:

- q35 machine,
- IDE/SATA-compatible disk attachment (`if=ide`) rather than VirtIO block,
- Intel e1000 emulated NIC rather than VirtIO networking,
- standard VGA rather than VirtIO VGA,
- OVMF/UEFI by default,
- KVM acceleration when available and accessible.

VirtIO can be introduced later as an optional high-performance test profile together with an explicit driver-injection path. It is not the baseline installer-validation hardware.

## Related commits

- `96cb6edd390c62a1e138a945dd78699964a9a58e` — use Windows-compatible emulated hardware in QEMU tests
- `63261e7207b45f57d7d41bc74e77617f3f6fe5a9` — add regression test that the baseline QEMU command does not depend on VirtIO

## Validation status

Code and regression test are committed. Do not claim runtime QEMU success until the user pulls these commits, the tests pass, and a genuine FX11 ISO is actually booted under OVMF.
