# Checkpoint — single-flow FX11 installer UX

Date: 2026-09-14
Status: architectural/UX decision

## Decision

FX11 should feel like one coherent installer, similar to the polished experience of mainstream Linux installers: partitioning is one step inside the installation flow, not a separate product that the user must manually hand off from.

The user should not experience a visible chain such as `GRUB -> GParted -> special Continue shortcut -> reboot -> separate installer` as the normal path.

Target UX:

```text
GRUB
  -> FX11 Installer
      -> choose install mode / disk
      -> partitioning step
          -> guided layout handled by FX11
          -> Custom launches GParted as a tool
          -> closing GParted returns to the same FX11 Installer
      -> re-detect and validate ESP / MSR / Windows / Recovery
      -> summary / confirm
      -> install
      -> hidden technical transition to WinPE if required
      -> DISM / BCDBoot / WinRE / FX Boot Manager
      -> OOBE
```

## GParted role

- GParted remains an upstream-attributed partitioning tool (`FX Partition Manager — powered by GParted`).
- It is not responsible for transferring control to the Windows installer.
- In the final UX it should be launched by the parent FX11 Installer for Custom partitioning and return to that parent flow when closed.
- Guided modes should increasingly use deterministic `sgdisk` / `parted` logic without opening GParted.

## Technical split

The user-facing FX11 Installer can run in a Linux live environment and own the full UI/state machine.

WinPE remains the preferred deployment engine for the Windows-specific final stage for now, because native Windows tools provide the safest path for DISM image application, BCDBoot and WinRE configuration.

The Linux -> WinPE transition should be an implementation detail, not a second visible installer product.

## Consequence

Existing v5/v6 work on GRUB, GParted Live and WinPE is still useful, but the normal UX direction changes: remove dependence on a special `Continue to FX11 Installer` desktop icon inside GParted as the primary handoff mechanism.
