# FX11 Builder development order — Windows-hosted first, Linux-hosted later

> **OWNER CLARIFICATION — 2026-10-21, overall FX project priority:** **P1 FX Linux (Fedora KDE first, LMDE possibly later)**; **P2 FX11 Builder running on Windows**; **P3 FX11 Builder running on Linux**. The earlier *Windows-first* sequence applies **within FX11 builder development only**, not to the overall FX project portfolio. Previous historical content below is preserved. See [the latest FX Linux-first priority decision](https://github.com/FenixMint/FX11-Builder/blob/main/docs/decisions/2026-10-21-FX-LINUX-FIRST-PORTFOLIO-PRIORITY.md).


Date: 2026-10-21  
Status: **OWNER PREFERRED SEQUENCING / DOCUMENTATION-ONLY**.

## Decision source

OWNER prefers developing an **FX11 Windows image builder running on Windows first**, and completing the **Linux-hosted implementation later**, because the Windows-hosted route may yield an end-to-end usable builder sooner.

This is a development sequencing decision, not a cancellation of `FenixMint/FX11-Builder` and not a claim that the Windows path has already been validated.

The Windows/PowerShell generation is recorded in `FenixMint/FenixMint-FX11-legacy`, with its Native Builder, Retrofit, Agent, Fenix System, visual UX and knowledge-base work. Keep this separate from the `FX11-Builder` Linux-native/offline pipeline.

## Preserve all work in this repository

**Nothing in this decision replaces or removes:**
- the existing Linux-native ISO build/inspect/validate commands, WIM/ESD work, hashes, build manifests or audit;
- WinPE launcher, FX Partition Manager, FX Boot Manager/GRUB, installer handoff and related safety design;
- test suite, historical documents, roadmap, code, branches or prototypes.

Maintain the current test/pre-release status and truthful limitations. No unverified real ISO build/install may be called accepted.

## Shared product contract, host-specific implementation

Proposed alignment (not yet implemented):
- common, versioned **profiles/policy, safety rules, manifests, hashes, diagnostics, output/acceptance criteria**, where technically meaningful;
- **Windows host**: native Windows image servicing path through supported mechanisms including DISM/PowerShell/ADK as selected by reviewed design;
- **Linux host**: existing Linux-native tooling and its own explicit mechanisms; do not pretend Windows servicing interfaces are available natively on Linux;
- compare expected resulting-system behavior in VM and real-media tests, rather than requiring byte-identical ISO output across hosts;
- Linux builder development resumes / intensifies after a Windows-hosted reference is successfully demonstrated and a separate scope is approved.

## Do not confuse two Linux tracks

1. **FX11 Builder on Linux**: Linux as the *host creating a customized Windows installation image*.
2. **FX OS Linux**: a customization/modification layer on Fedora KDE and later possibly LMDE, **not** a self-maintained Linux distribution for now.

These are distinct products/capabilities, and the new Windows-first priority concerns **(1)**, not postponing all FX OS Linux desktop work.

## Next checkpoint

Inventory the Windows/PowerShell Native Builder in FX11 Legacy, identify the smallest non-destructive genuine-Windows-ISO -> candidate image -> VM boot -> security/serviceability verification path, and establish which policies/audit artifacts can be shared later. No code changes or running tests are authorized solely by this document.

Related: [FX OS family decision](2026-10-21-FX-OS-FAMILY-AND-FX11-BUILDER.md) and [Windows-first plan in FX11 Legacy](https://github.com/FenixMint/FenixMint-FX11-legacy/blob/main/docs/decisions/2026-10-21-FX11-WINDOWS-FIRST-BUILDER-SEQUENCING.md).

No implementation or test execution is claimed.
