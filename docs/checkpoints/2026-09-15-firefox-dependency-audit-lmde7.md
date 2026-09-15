# LMDE 7 Firefox dependency audit — 2026-09-15

Source ISO: `/home/hype/Pobrane/lmde-7-cinnamon-64bit.iso`

Observed installed browser package:
- `firefox 143.0.3~linuxmint1+gigi`

Reverse dependency scan across installed packages showed:

- `mintchat` has a hard dependency on `firefox`:
  - `Depends=python3 (>= 3.3), python3-gi, webapp-manager, firefox`
- `libreoffice-help-en-us` only recommends a browser through alternatives:
  - `firefox-esr | epiphany-browser | konqueror | chromium | firefox`
- `mint-meta-cinnamon` and `mint-meta-core` did not directly reference Firefox in this installed-package dependency scan.
- Firefox provides `gnome-www-browser` and `www-browser`.
- Firefox has `Pre-Depends: debian-system-adjustments (>= 2021.12.16)`.

Project decision remains unchanged:
- LibreWolf will be the default FX browser.
- Firefox remains installed as a secondary/compatibility browser.
- Do not remove Firefox just to reduce duplication; on this LMDE 7 source image, removing it would at minimum affect `mintchat` unless dependencies/packages are changed.
- No need to alter Mint packages solely to remove Firefox.

Optional curiosity test for later: run an APT removal simulation (`apt-get -s remove firefox`) inside the extracted root to see the exact package transaction proposed by APT.
