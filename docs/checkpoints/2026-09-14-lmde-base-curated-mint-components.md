# Checkpoint — LMDE base + curated Mint components

Date: 2026-09-14

## Correction
LMDE 7 is **not** a rolling-release distribution. It is a long-term-support Linux Mint edition based on Debian 13 (Trixie) stable. Major LMDE generations move between Debian stable releases (for example LMDE 6 -> 7 via a dedicated upgrade process).

## Direction under consideration
Use LMDE 7 / Debian 13 stable as the FX Live base, then selectively bring in useful improvements from the Ubuntu-based Linux Mint line.

Important rule: do **not** mix Ubuntu binary repositories into LMDE/Debian globally. That risks dependency and ABI conflicts (a FrankenDebian-style system).

Preferred ways to combine the two worlds:
- use LMDE/Debian stable as the system ABI and package base;
- port/rebuild selected Mint components from source against Debian/LMDE;
- reuse configuration, patches, themes, XApps and installer UX ideas where licensing allows;
- use Debian backports or another explicitly controlled mechanism for newer kernel/firmware/tooling when required;
- use Flatpak/AppImage for user applications where isolation is useful;
- only accept individual third-party .deb packages after dependency/ABI validation;
- never enable Ubuntu repositories as general package sources on the LMDE base.

This mirrors Linux Mint's own practice: improvements developed for the Ubuntu-based Mint line are ported to LMDE on top of the Debian package base.

## Product architecture
FX11 and future FX Linux remain separate products. FX Live may become the shared technical base, but the current implementation priority remains FX11 Installer.

## Status
Architecture candidate, not yet a final base selection. Requires a practical LMDE 7 FX Live prototype and comparison against regular Mint 22.x before locking the base.
