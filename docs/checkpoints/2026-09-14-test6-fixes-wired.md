# Test6 fixes wired after physical test5

Date: 2026-09-14
Status: CODE WIRED / NOT YET LOCALLY OR PHYSICALLY VALIDATED

Physical test5 established three separate results:

- GParted Live now starts automatically without the earlier graphics/resolution questions (`gl_batch` physical pass).
- GRUB enters a higher-resolution graphical terminal, but the intended FX11 theme/background/logo still does not render.
- `FX11 Installer` still fails on physical UEFI with `error: unknown error.` when the Microsoft EFI loader is chainloaded from the ISO filesystem.
- The intended `Continue to FX11 Installer` action is not visible in GParted Live.

Root-cause findings and test6 direction:

1. The GRUB build/config had `gfxterm`, PNG and font support but did not include/load `gfxmenu`, which is required for the GRUB graphical menu/theme viewer. Test6 now includes `gfxmenu` in the standalone EFI module set and explicitly loads it in `grub.cfg`.

2. GParted Live uses Fluxbox plus idesk. A freedesktop `.desktop` file alone is not the right primary desktop integration. The FX handoff hook now installs an idesk launcher and a Fluxbox root-menu entry, while retaining the `.desktop` file only as a fallback.

3. Chainloading `bootmgfw.efi` directly from the ISO9660 tree is abandoned for the test6 path. Test6 builds a real FAT-resident WinPE boot environment. The builder starts from the original Microsoft EFI boot image, preserves its Microsoft EFI/BCD files, overlays FX GRUB and the FX theme, and adds the customized `sources/boot.wim` plus `boot/boot.sdi`. A `/EFI/FX11/winpe-ready` marker identifies this FAT volume. `FX11 Installer` searches for that marker and chainloads `/EFI/Microsoft/Boot/bootmgfw.efi` from the same FAT filesystem.

4. The ISO9660 data tree continues to carry the selected `install.wim`, FX11 manifest and provisioning payload. Once WinPE starts, the existing FX11 installer can discover that media volume separately.

5. The combined EFI/WinPE FAT image is dynamically sized for the source Microsoft EFI image, boot.wim, boot.sdi, theme and reserve space. This deliberately makes test6 larger than test5. It is a physical-USB validation path; later media-size/DVD optimization remains separate work.

Code touched:

- `src/fx11/media_efi.py`
- `src/fx11/media_boot.py`
- `assets/gparted/90-fx11-continue`
- `scripts/repack-fx11-usb-hybrid.sh`
- `tests/test_media_boot.py`
- `tests/test_media_efi.py`
- `tests/test_gparted_handoff.py`

Important validation boundary:

- These changes are committed but have not yet been proven by the user's local pytest/repack run.
- The new mtools copy of the original Microsoft EFI tree and the large FAT image must be validated before test6 is written to USB.
- Do not call the FX11 theme, GParted handoff, FAT WinPE boot, DISM deployment, BCDBoot or OOBE successful until observed on physical hardware.
