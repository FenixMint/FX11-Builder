# FX roadmap

This document records longer-term direction that should not be confused with currently completed functionality.

## Phase 1 — make FX11 genuinely usable

Immediate priorities remain:

1. build a real FX11 ISO from genuine Windows 11 media,
2. validate the dual-environment installer path,
3. use the FX-branded GParted-based environment as the main graphical FX Partition Manager,
4. retain the native text FX Partition Manager as recovery/fallback and an independent development path,
5. complete direct WinPE image deployment,
6. configure Windows boot/WinRE/OOBE correctly,
7. finish FX Boot Manager integration,
8. validate on QEMU/OVMF and reference real hardware,
9. compare stock Windows 11 vs FX11 resource use and responsiveness,
10. keep provenance, licensing and security auditing visible.

## Phase 2 — broaden Linux build-host support

Current maintained host family:

- Linux Mint,
- LMDE,
- Debian.

FX11 should evolve from a Debian-specific bootstrap into a distro-adapter model.

Desired architecture:

```text
FX11 Builder core
    |
    +-- host detection
    +-- dependency capability checks
    +-- package-name mapping
    +-- package-manager adapter
    +-- distro-specific exceptions only where necessary
```

Candidate next host families, subject to real testing:

1. Ubuntu-family systems,
2. Fedora-family systems,
3. openSUSE,
4. Arch-family systems.

Possible later targets can be added only when useful and maintainable.

A host distribution is not called supported merely because the Python code starts there. Support means at minimum:

- dependencies install correctly,
- `fx11 doctor` passes,
- unit tests pass,
- synthetic E2E build passes,
- genuine Windows ISO inspection/build succeeds,
- produced media matches the normal FX11 validation expectations.

The goal is to keep the builder core distro-neutral and isolate package-manager differences.

## Phase 3 — stable FX11 product layer

Once installation is stable, continue with:

- FX11 First Run,
- FX11 Control Center,
- privacy/status checks,
- application selection,
- Start/taskbar configuration,
- boot-manager configuration,
- Multi-OS Guide,
- production Secure Boot chain,
- runtime security auditing,
- reproducible release documentation.

## Future sibling project — FX Linux

If FX11 proves the FX build/install model works well, explore a separate sibling project named **FX Linux**.

This is an idea/roadmap item, not a current implementation commitment.

### Principles to carry over

- **Your System. Your Rules.**
- transparent choices rather than hidden policy,
- reproducible builds,
- visible upstream provenance,
- honest licensing and attribution,
- FX Partition Manager,
- FX Boot Manager,
- multi-OS friendliness,
- privacy controls that are understandable and reversible,
- strong support for older/weaker hardware where technically sensible,
- no unnecessary vendor lock-in.

### What is intentionally undecided

Do not choose a Linux base distribution prematurely.

Potential questions for later evaluation include:

- Debian/Ubuntu base vs Fedora/openSUSE/Arch-family base,
- immutable vs traditional package model,
- desktop environment,
- release cadence,
- installer architecture,
- Secure Boot and signing,
- hardware enablement,
- update/recovery model,
- how much code can be shared cleanly with FX11 components.

### Project boundary

FX Linux should be a separate product/repository when it becomes real.

Do not turn FX11 Builder into a mixed Windows/Linux distribution repository. Shared FX libraries/components may be split out later if that becomes technically justified.

## Provenance rule for future FX projects

The standard established in FX11 should carry forward:

- say which upstream project inspired a feature,
- say which upstream code/component is redistributed,
- keep source/license obligations,
- publish FX modifications where required,
- distinguish original FX work from integration work,
- do not erase upstream names under FX branding.

That is a product principle, not only a legal checklist.
