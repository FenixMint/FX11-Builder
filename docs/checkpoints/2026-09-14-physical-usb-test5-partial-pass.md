# Physical USB test5 — partial pass

Date: 2026-09-14
Status: PARTIAL PASS / FOLLOW-UP REQUIRED

Physical UEFI boot of `FX11-25H2-PL-x64-Home-test5-hybrid.iso` was tested on the HP low-end reference laptop.

Observed:

- FX GRUB boots from the physical USB.
- The menu contains `FX Partition Manager`, `FX11 Installer`, and `UEFI Firmware Settings`.
- GRUB now enters a graphical `gfxterm`-style menu, so the UX is improved compared with the earlier plain text stage.
- The intended FX11 theme background/logo is still not rendered. The menu remains close to the default GRUB graphical menu.
- `FX Partition Manager` launches GParted Live automatically and the earlier graphics/resolution questions are gone. `gl_batch` is therefore physically confirmed on this hardware.
- The GParted environment does not expose the intended `Continue to FX11 Installer` handoff action. The current `.desktop` launcher approach does not match GParted Live's Fluxbox/idesk desktop mechanism.
- Selecting `FX11 Installer` from GRUB still fails. The physical screen reports `error: unknown error.` followed by `Press any key to continue...` while chainloading the preserved Microsoft `bootmgfw.efi` from the ISO filesystem.

Conclusions:

1. GParted automatic graphical startup is now a physical pass.
2. GRUB graphical terminal is a partial pass, but the real FX11 theme is not yet loaded.
3. Direct GRUB chainload of the Microsoft EFI loader from the ISO filesystem is not a reliable WinPE boot path on the tested hardware.
4. The next USB test must use a real FAT-resident WinPE boot environment rather than chainloading `bootmgfw.efi` from the ISO9660 tree.
5. The GParted handoff should integrate with GParted Live's actual Fluxbox/idesk desktop model instead of relying on freedesktop `.desktop` files alone.

Implementation direction for test6:

- include/load GRUB `gfxmenu` so the configured theme can actually render;
- add an idesk launcher for `Continue to FX11 Installer` and keep a Fluxbox-accessible fallback;
- construct the FX11 EFI FAT image from the original Microsoft EFI boot image, preserve its Microsoft boot files/BCD, overlay FX GRUB/theme, and add `boot/boot.sdi` plus the customized `sources/boot.wim` on the FAT volume;
- chainload the Microsoft boot manager from that FAT volume, not from the ISO filesystem;
- keep the main FX11 ISO9660 data tree as the source of `install.wim` and provisioning payload, to be discovered after WinPE starts.

This checkpoint records observed physical behavior only. Full WinPE startup, disk visibility, DISM deployment, BCDBoot and OOBE remain unvalidated.