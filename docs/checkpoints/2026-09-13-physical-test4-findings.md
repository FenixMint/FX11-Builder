# Physical USB test findings — 2026-09-13

Observed on real hardware after the hybrid USB work:

- Physical USB boot reaches FX GRUB.
- FX Partition Manager now starts GParted Live automatically with no manual X/graphics prompts. The `gl_batch` direction is confirmed on hardware.
- The graphical FX11 GRUB theme was not visible; the boot menu still appeared as the plain/raw GRUB presentation. Theme integration therefore remains unconfirmed and needs a more robust media-boot implementation.
- There is no satisfactory handoff/continue path from the GParted environment to the FX11 installer yet. A user should not have to infer the next boot step.
- Selecting `FX11 Installer` from the FX GRUB menu fails with the firmware/GRUB message: `Error: cannot load image.` followed by `Press any key to continue...`.

## Interpretation

The `/bootmgr.efi` direct chainload target used for the diagnostic iteration is not accepted in this real boot path and must not be treated as a working WinPE entry.

The next iteration should:

1. restore the preserved Microsoft removable-media EFI loader as the WinPE chainload target (`/efi/microsoft/boot/bootmgfw.efi` in the rebuilt media tree), rather than chainloading `/bootmgr.efi` directly;
2. rebuild the FX media EFI image during the fast repack so the tested GRUB binary and graphical assets are current, instead of relying on the older EFI image while only refreshing files in the ISO filesystem;
3. stage the FX11 GRUB theme in the EFI FAT image as well as in the ISO tree and provide a direct background-image fallback, so failure of the richer GRUB theme parser does not regress to a black screen;
4. design a clear `Continue to FX11 Installer` handoff from GParted. A reboot-to-installer marker on the writable `FX11BOOT` FAT partition is the preferred direction, with the marker later cleared by WinPE.

This checkpoint records observed physical behavior. It does not claim the WinPE or graphical-theme fixes are validated yet.
