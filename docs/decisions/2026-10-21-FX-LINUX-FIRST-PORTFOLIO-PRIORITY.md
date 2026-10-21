# OWNER decision — FX Linux first in the FX project portfolio

Date: 2026-10-21  
Status: **OWNER DECISION — ACTIVE PRIORITY CLARIFICATION**, documentation only.

## Explicit OWNER correction

Following the earlier decision to develop FX11 Builder **on Windows before Linux**, OWNER clarified:

> "ale priorytet ma FX LInux"

**Binding interpretation: FX Linux / FX OS Linux is the HIGHEST OVERALL PRIORITY across this FX operating-system family.**

The prior `Windows-hosted first` decision refers **only to the internal execution order of the two FX11 Windows-image builder host implementations**. It is **not** a statement that FX11 development outranks FX Linux.

## Priority order

1. **P1 — FX Linux / FX OS Linux**: develop the customizable Linux desktop and its modules on Fedora KDE Plasma first, inspired in part by experience with COSMIC and years of Cinnamon; possible LMDE adaptation later. Attractive, comfortable UI and reusable, auditable modification modules over existing Linux distributions are central. A self-maintained standalone Linux distribution is not the current objective.
2. **P2 — FX11 Builder running on Windows**: continue the independent Windows image builder from the existing Windows/PowerShell generation with security, compatibility and serviceability preserved. Use Windows-native tooling where appropriate.
3. **P3 — FX11 Builder running on Linux**: preserve the existing Linux-native/offline builder code, tests, designs and history, and mature it later, informed by the validated Windows-hosted implementation. Not abandoned.

These ranks set **relative resource/attention priority**, not fixed release dates or permission to abandon existing work. A scoped maintenance or safety fix in a lower-priority line can still be required.

## Critical distinctions

- **FX Linux (FX OS Linux)** = customization/UX/system modules on existing Linux operating systems such as Fedora and, later potentially, LMDE.
- **FX11 Builder on Linux** = a program running on a Linux host that creates a customized **Windows** installation image. It is NOT FX Linux itself.
- **FX11 Builder on Windows** = a program running on Windows to create a customized **Windows** installation image.
- **FX NEXUS** remains a separate business/application project, outside this priority decision.

## Preservation and implementation boundaries

- This new priority **clarifies** earlier project-direction documentation and supersedes only a possible mistaken interpretation that FX11 is the top FX OS priority.
- It **does not delete or overwrite earlier architecture, historical checkpoints, commits, branches, or technical work**. Previous documents remain intact except for additive cross-reference notices.
- No repository merge, rename, public product release, installed OS modification, partition/boot change or destructive action is authorized.
- Implementation milestones, supported Fedora/KDE/LMDE versions, installation packaging and test results remain to be separately designed, implemented and verified.
- The shared principle stays **Your System. Your Rules.**

## Related decisions

- [Family-level FX OS direction](2026-10-21-FX-OS-FAMILY-AND-FX11-BUILDER.md)
- [FX11 host ordering: Windows first, Linux later](2026-10-21-WINDOWS-FIRST-SEQUENCING-NO-LOSS-OF-LINUX-WORK.md)
- [FX11 Legacy Windows-host implementation order](https://github.com/FenixMint/FenixMint-FX11-legacy/blob/main/docs/decisions/2026-10-21-FX11-WINDOWS-FIRST-BUILDER-SEQUENCING.md)

**This commit documents an OWNER decision; no implementation or test execution is claimed.**
