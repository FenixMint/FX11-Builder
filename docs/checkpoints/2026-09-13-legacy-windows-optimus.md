# Checkpoint — legacy Windows branches and XP Optimus target

Date: 2026-09-13

Decision:

- FX11 remains the current priority.
- After FX11 is stable enough, investigate separate FX build/install branches for Windows 7 and Windows XP using user-provided licensed source media.
- Windows 7 is expected to be the easier first compatibility target.
- Windows XP is a specialist legacy-software target and should be treated as offline/isolated by default.

Specific XP research target:

- NVIDIA GeForce GT 525M,
- Intel integrated graphics (likely HD Graphics 3000 on Sandy Bridge systems),
- Optimus/hybrid graphics notebook.

Research finding recorded today:

- official NVIDIA XP notebook drivers exist that list GT 525M,
- official Intel XP drivers exist for HD Graphics 3000,
- official NVIDIA Optimus documentation requires Windows 7 or later.

Therefore the key problem is not simply the presence of XP drivers for both GPUs. The key problem is the exact notebook display topology and the missing XP Optimus switching/render-copy path.

Next required data before implementation work:

- exact notebook model,
- BIOS version,
- CPU/Intel GPU,
- NVIDIA and Intel PCI device + SUBSYS IDs,
- whether the internal LCD is wired to Intel only,
- whether an external display output is wired to NVIDIA,
- whether there is a hardware mux or BIOS discrete-only mode.

Canonical technical notes: `docs/LEGACY_WINDOWS.md`.
