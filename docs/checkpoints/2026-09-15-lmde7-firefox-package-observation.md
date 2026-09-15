# LMDE 7 Firefox package observation — 2026-09-15

Read-only inspection of the verified LMDE 7 Cinnamon ISO (`/home/hype/Pobrane/lmde-7-cinnamon-64bit.iso`) showed these installed packages in `live/filesystem.packages` when filtering for Firefox/meta/browser related names:

- `firefox` `143.0.3~linuxmint1+gigi`
- `mint-meta-cinnamon` `2023.09.08.1+lmde6`
- `mint-meta-core` `2023.09.08.1+lmde6`
- `webapp-manager` `1.4.3`

This proves only that these packages are present in the LMDE 7 Live filesystem; it does **not** by itself prove that Firefox is a dependency of either Mint metapackage.

FX policy remains:
- LibreWolf will be the default browser in FX.
- Firefox remains installed as a secondary/fallback browser and for compatibility.
- There is no current goal to remove Firefox.
- A reverse-dependency / metapackage audit may be done for curiosity and documentation before later cleanup decisions.
