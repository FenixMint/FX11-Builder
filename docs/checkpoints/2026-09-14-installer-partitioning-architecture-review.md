# Installer partitioning architecture review — 2026-09-14

## Why this review

Physical FX11 media tests showed that a loose chain of GRUB -> GParted -> handoff hook -> reboot -> WinPE works only partially and produces an awkward user experience. Before continuing with more handoff-specific fixes, the Linux Mint and Calamares installer architectures were reviewed to separate two ideas that look similar in the UI but are technically different:

1. a standalone GParted process launched by an installer;
2. a partitioning page implemented directly inside the installer.

## Linux Mint 22.x / Ubiquity

The standard Linux Mint 22.x installer uses Linux Mint's maintained Ubiquity fork. Its partitioning workflow is integrated into the main installer UI. The Ubiquity `partman` plugin loads its own GTK pages (`stepPartAsk.ui`, `stepPartAuto.ui`, `stepPartAdvanced.ui`, `stepPartCrypto.ui`) and presents automatic, resize and manual partitioning as pages of the same installer window.

This integrated UI is not an embedded GParted application. It is Ubiquity's own GTK partitioning frontend backed by Debian partman and related installer components.

This is the UX model that should guide FX11: one installer, one navigation model, one state machine.

## LMDE / live-installer

Linux Mint's `live-installer` uses its own GTK partition list built with `python-parted`, but its advanced manual edit path explicitly starts `gparted ... &`. That is a separate process and separate window. This is a useful fallback model, but it is not the seamless experience desired for FX11.

## Calamares

Calamares follows the integrated model as well. Partitioning is a user-visible installer module and uses KPMCore, the same partitioning library family used by KDE Partition Manager. It does not need to embed the KDE Partition Manager application itself.

## FX11 direction

Adopt a hybrid of the integrated-installer patterns:

- FX11 Installer is the parent application and owns navigation/state.
- Normal workflows (`FX11 only`, `FX11 + Other OS`) use an integrated FX partitioning page and deterministic backend logic (`parted`/`sgdisk`/filesystem tools).
- The integrated page shows the current disk layout, proposed layout, ESP/MSR/Windows/Recovery status, sizes and destructive-operation warnings.
- GParted remains available as an advanced `Custom` editor rather than being the parent workflow.
- If GParted is launched for Custom mode, the installer waits for it to close, rescans all disks, validates the resulting layout, and returns to the same FX11 Installer page.
- Do not attempt to embed the standalone GParted window as if it were an installer widget. If future work forks GParted code, treat that as a separate licensing/maintenance decision.
- WinPE remains the preferred deployment engine for DISM, BCDBoot and WinRE. The Linux-side FX11 Installer prepares and validates the target and hands off an explicit install context.

## Target UX

```text
FX11 Installer
  1. Language
  2. Installation mode
  3. Target disk
  4. Partitioning
       - FX11 only
       - FX11 + Other OS
       - Custom -> GParted -> return/rescan
  5. Validation / summary
  6. Install
       -> WinPE deployment engine
       -> DISM /Apply-Image
       -> BCDBoot
       -> WinRE
       -> FX Boot Manager
  7. Reboot / OOBE
```

The key design principle is that GParted is a tool used by FX11 Installer, not the application that owns the installation flow.
