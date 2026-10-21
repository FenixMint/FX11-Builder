# OWNER decision — FX OS family and FX11 Builder direction (2026-10-21)

> **OWNER CLARIFICATION — 2026-10-21, overall FX project priority:** **P1 FX Linux (Fedora KDE first, LMDE possibly later)**; **P2 FX11 Builder running on Windows**; **P3 FX11 Builder running on Linux**. The earlier *Windows-first* sequence applies **within FX11 builder development only**, not to the overall FX project portfolio. Previous historical content below is preserved. See [the latest FX Linux-first priority decision](https://github.com/FenixMint/FX11-Builder/blob/main/docs/decisions/2026-10-21-FX-LINUX-FIRST-PORTFOLIO-PRIORITY.md).


Status: **OWNER DECISION (direction)** + **PLANNED (implementation)**. Additive project record; preserves previous architecture, source code, historical decisions, and checkpoints.

## Source and interpretation

OWNER expressed in the ongoing FX OS discussion:
- `FX OS` originally meant an improved Tiny11 / Windows experience; the vision now includes both Linux modifications and Windows.
- For now OWNER cannot maintain an independent Linux distribution. Instead, FX OS Linux should be a **modification/configuration layer over an existing distribution**.
- OWNER has moved to **Fedora** as the present Linux base (target desktop: configurable KDE Plasma, with inspiration from COSMIC); **LMDE** is a possible later base.
- **FX11 will have our own builder** rather than remaining a Tiny11-derived collection of tweaks.
- The Windows operating-system generation changes less frequently than the releases of Linux distributions; this should influence maintenance and architecture.
- Previous GitHub project history must **not be deleted or overwritten** to accommodate the new direction.

These points are product direction, not evidence that all functionality has already been implemented or fully tested.

## Architectural separation

### FX OS — shared vision / identity

A coherent, usable, visually distinctive desktop and system customization experience across Windows and Linux.

Common design principles:
- user autonomy: **Your System. Your Rules.**
- attractive, not overly flat, but practical and comfortable for everyday work;
- independent, selectable visual/UX and optimization/privacy capabilities;
- reversible, explainable changes and safe defaults;
- no assumption that users must run one specific Linux distribution or Windows image.

**FX OS is an umbrella concept**, not currently a claimed independent Linux distribution or a completed unified product. Repository ownership and exact naming/packaging are **OPEN** until separately decided by OWNER.

### FX OS Linux — distribution adaptation track

**OWNER DECISION / PLANNED:**
- Modify upstream distributions rather than fork and maintain a complete Linux distribution for now.
- Start with **Fedora KDE Plasma**; anticipate an LMDE adaptation later.
- Keep a shared design/configuration layer, and explicit distro-specific adapters for package names, repositories, system services and release differences.
- Treat faster-paced Linux distribution and desktop releases as a maintenance concern: verify compatibility per release, test migrations, preserve rollback, and do not pretend Fedora and LMDE are identical.
- COSMIC remains valuable inspiration / a prior practical experience; no requirement to copy COSMIC code or its architecture into KDE.
- Prefer reproducible, auditable configuration modules over one-off manual edits.
- Existing components and prototypes, including Fenix Night Light / Fenix System / GRUB theme work, may be evaluated for integration **without declaring them finished, merged or distro-agnostic**.

Linux edition names, package/installer format, exact repository location, supported distro versions, and release cadence remain **OPEN**.

### FX11 / FX OS Windows — own builder line

**OWNER DECISION: build an independent FX11 Builder.** Preserve and continue the known work instead of starting from zero.

Historical/current architecture that is **not superseded by this decision**:
1. `FenixMint/FenixMint-FX11-legacy`: Windows/PowerShell generation, including FX11 Native, Tiny Retrofit, Windows Retrofit, Agent/Guard, Fenix System and visual capability. Historical code, tests and decisions remain intact.
2. `FenixMint/FX11-Builder`: distinct Linux-native/offline builder project using original Windows media, WIM tooling, manifests, boot/partition/installer work and audits. Its existing code and documentation remain intact.

The new owner statement **does not require merging these builders** or deleting either one. Technical consolidation/roadmap is an **OPEN architecture decision** requiring separate review.

FX11 should build from legitimate user-supplied Microsoft Windows media, apply controlled, traceable and selectively configurable changes, and preserve security, updates, recovery and required compatibility. Tiny11 is acknowledged as historical inspiration, **not** a requirement to port or depend on it.

Because new Windows system generations are less frequent than distro releases, FX11 may work in deeper Windows-version-specific build/validation cycles; nevertheless Windows feature updates, drivers, APIs and servicing still require recurring compatibility testing. Do not assume a longer version cadence eliminates maintenance.

## Preservation / boundaries

- **No deletion, rewriting of history, repo merges, renames or migrations are authorized by this note.**
- Earlier records remain historical truth until an explicit, dated, scoped superseding OWNER decision.
- Existing FX11 safety doctrine remains: `DISCOVER -> AUDIT -> CLASSIFY -> PLAN -> APPROVE -> APPLY -> VERIFY -> GUARD`; **FX11 Quality > FX11 Uniformity**.
- Modifications to installed systems, partition tables, bootloader paths, updates, privacy/security controls and users' data require their own approved implementation and test plan.
- **FX NEXUS is a separate application/business platform**, not an FX OS submodule or repository to change under this direction.

## Suggested next design work — proposal, not authorization to change code

1. Define a versioned FX OS visual/UX contract and prototype it on Fedora KDE: top panel, left dock, application menu, visual depth, system monitoring.
2. Identify reusable configuration vs Fedora/LMDE-specific adapters, plus supported versions and uninstall/rollback model.
3. Inventory existing FX11 Windows/PowerShell and Linux-native builder capabilities and gaps; choose roadmap without losing either line's history.
4. Establish a dedicated future FX OS project/repository boundary only with an explicit OWNER decision.
5. Put tested compatibility matrices and concrete implementation status in their respective project repositories.

## References

- [FX11 Builder README](../../README.md) and [canonical project history](../PROJECT_HISTORY.md)
- [FX11 Legacy project](https://github.com/FenixMint/FenixMint-FX11-legacy)
- [FX11 Legacy preservation checkpoint](https://github.com/FenixMint/FenixMint-FX11-legacy/blob/main/docs/checkpoints/FX11-KNOWLEDGE-CP1-2026-10-07.md)
- [Fenix Night Light](https://github.com/FenixMint/fenix-nightlight)

Documentation-only checkpoint on 2026-10-21. **No implementation, migration, test run or local deployment is claimed by this document.**
