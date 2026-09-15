# 2026-09-15 — LMDE 7 source image verified

The first FX Live / FX Linux proof-of-concept now has an identified and checksum-verified LMDE source ISO.

## Local source image

- Path: `/home/hype/Pobrane/lmde-7-cinnamon-64bit.iso`
- Filename: `lmde-7-cinnamon-64bit.iso`
- Size: `2,960,867,328` bytes
- `file` description: `ISO 9660 CD-ROM filesystem data (DOS/MBR boot sector) 'LMDE 7 Cinnamon 64-bit' (bootable)`
- Volume ID: `LMDE 7 Cinnamon 64-bit`
- SHA256: `520b9de3e06871d69292f0e82a5979b62088ad83fdf4dce1d19100118a7033e4`

## Checksum verification

The local SHA256 exactly matches the checksum published for `lmde-7-cinnamon-64bit.iso` in the Linux Mint Debian mirror checksum file.

This source image is therefore accepted as the canonical input for the first FX Live PoC unless deliberately replaced by a newer validated image later.

## Boot structure observed with xorriso

`xorriso -toc` reports:

- El Torito boot information
- MBR isohybrid
- GPT
- APM
- BIOS boot catalog: `/isolinux/boot.cat`
- BIOS boot image: `/isolinux/isolinux.bin`
- UEFI boot image: `/boot/grub/efi.img`
- Rock Ridge and Joliet filesystem extensions
- one ISO session
- 1,445,736 data blocks (~2824 MiB)

This is useful for the remaster strategy because the source image is already hybrid and supports both legacy BIOS and UEFI boot paths.

## Current status

No remastering has been performed yet. The source image has only been identified and inspected.

The attempted `xorriso -find / -maxdepth 2 -type f -print` command returned no visible output, so the next inspection should use direct directory listings (`-ls` / `-lsl`) or a corrected xorriso `-find ... -exec lsdl` form before making assumptions about the exact live filesystem path.

## Next inspection targets

Confirm exact locations and names for:

- live SquashFS
- kernel
- initrd
- GRUB configuration
- isolinux configuration
- any LMDE live-session and installer assets relevant to FX Live reuse
