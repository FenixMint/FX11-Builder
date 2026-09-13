# FX11 installation-media GRUB theme wired — 2026-09-13

## Decision

The physical USB boot proved that raw black GRUB is not acceptable as the normal FX11 first-run experience. The approved direction is a dark FX11 visual identity with a green/teal accent, large FX11 mark, Fenix attribution and a simple left-side menu inspired by the cleanliness of Linux Mint GRUB without copying its theme.

Author/project mark: `Fenix` — not `FenixMint`.

## Implemented for the next physical test

- Added `src/fx11/media_theme.py`.
- The media theme is generated deterministically with Python stdlib only; no external image dependency is required.
- Theme assets:
  - `/FX11/media/theme/theme.txt`
  - `/FX11/media/theme/background.png`
  - `/FX11/media/theme/unicode.pf2`
- GRUB switches to `gfxterm` when the staged font is available and loads the FX11 theme.
- Menu labels are simplified to:
  - `FX Partition Manager`
  - `FX11 Installer`
  - `UEFI Firmware Settings`
- `powered by GParted` is kept as a small theme attribution instead of part of the menu item title.
- Existing automatic GParted parameters (`gl_batch`, Polish locale and keyboard) remain in place.
- Existing WinPE diagnostic target remains `/bootmgr.efi` and still requires physical confirmation.
- `scripts/repack-fx11-usb-hybrid.sh` now refreshes both the GRUB config and the graphical theme so the visual change can be tested without rebuilding Windows WIM files.

## Important status

This checkpoint records code integration, not a runtime pass. The graphical theme still needs observation on real UEFI firmware. If gfxterm, PNG rendering or font loading behaves differently on a given firmware, the boot path must remain recoverable and be adjusted based on observed output.

Direct integration of the tested theme into the normal one-shot `fx11 build` output is the next step after physical confirmation of this media-theme iteration.
