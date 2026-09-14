# FX Live LMDE + Calamares PoC — start checkpoint

Date: 2026-09-14

## Direction

The GParted-Live-first architecture is superseded for the user-facing Linux stage.

Current target:

- LMDE 7 is the base candidate for FX Live and the future FX Linux foundation.
- Calamares is the installer framework candidate.
- One FX Live environment can route to separate installer profiles:
  - FX11 phase 1
  - FX Linux
  - Try FX / tools
- FX11 Windows-native deployment remains in WinPE after the Linux phase.
- Microsoft setup.exe is not run under Linux.
- Windows installation media is still supplied by the user; generated Windows ISOs are not published.

## First repository implementation

Added a first non-destructive proof-of-concept scaffold:

- `src/fx11/live.py`
  - shared `fx.mode=` contract
  - FX11 / FX Linux / Live modes
  - Calamares profile routing
- `live-overlay/usr/local/bin/fx-live-launcher`
  - reads `fx.mode=` from the kernel command line
  - falls back to a graphical Zenity chooser
  - starts the matching Calamares profile through `pkexec`
- `live-overlay/etc/xdg/autostart/fx-live-launcher.desktop`
  - starts the chooser in the live desktop session
- separate Calamares prototype profiles:
  - `/etc/fx/calamares/fx11`
  - `/etc/fx/calamares/linux`
- separate FX11 / FX Linux Calamares branding stubs.
- `scripts/build-fx-live-poc.sh`
  - takes an LMDE 7 ISO
  - extracts its live SquashFS
  - installs Debian Calamares + settings + Zenity + pkexec in the live rootfs
  - applies the FX overlay
  - rebuilds SquashFS
  - uses xorriso boot-equipment replay to create a modified ISO.

The FX Linux profile exposes the stock Calamares integrated partition page for UX evaluation, but the prototype intentionally has no destructive exec phase yet.

The FX11 profile does not yet use stock Linux partition semantics. A future `fxpartition` module will use KPMCore with Windows-aware ESP/MSR/NTFS/Recovery semantics and durable install-context output.

## EFI policy update

Guided FX11 layouts now use a 1 GiB EFI System Partition (`ESP_MIB = 1024`) instead of 300 MiB.

Policy:

- new guided layouts: one shared 1 GiB FAT32 ESP;
- prefer reusing an existing valid ESP for multi-boot;
- do not create additional ESPs unnecessarily;
- rules for when an existing smaller ESP should be expanded remain subject to physical validation.

## Status

Code and configuration scaffold are committed.

Not yet validated:

- build of the new LMDE-based PoC ISO;
- boot in QEMU;
- boot on physical hardware;
- Calamares configuration compatibility inside LMDE 7;
- xorriso replay result for LMDE's exact hybrid boot layout;
- graphical launcher appearance;
- any disk-changing installation flow.

Do not claim this PoC works until those checks are run.
