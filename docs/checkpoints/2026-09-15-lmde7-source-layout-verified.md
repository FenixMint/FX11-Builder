# LMDE 7 source layout verified — 2026-09-15

Source ISO used for the first FX Live proof-of-concept:

- Path used locally: `/home/hype/Pobrane/lmde-7-cinnamon-64bit.iso`
- File size: `2960867328` bytes
- SHA256: `520b9de3e06871d69292f0e82a5979b62088ad83fdf4dce1d19100118a7033e4`
- Volume ID: `LMDE 7 Cinnamon 64-bit`
- ISO type: ISO 9660, bootable, Rock Ridge + Joliet
- Boot structure detected by xorriso: El Torito + MBR isohybrid + GPT + APM
- BIOS boot image: `/isolinux/isolinux.bin`
- UEFI boot image: `/boot/grub/efi.img`
- Boot catalog: `/isolinux/boot.cat`

Verified top-level ISO directories/files:

- `.disk`
- `EFI`
- `boot`
- `dists`
- `efi.img`
- `isolinux`
- `live`
- `md5sum.README`
- `md5sum.txt`
- `pool`

Verified live payload:

- `/live/filesystem.squashfs` — `2441183232` bytes
- `/live/initrd.lz` — `144437070` bytes
- `/live/vmlinuz` — `12109760` bytes
- `/live/filesystem.packages`
- `/live/filesystem.packages-remove`
- `/live/filesystem.size`

Verified `/boot` contents:

- `/boot/grub/`
- `/boot/memtest.bin`
- `/boot/memtest.efi`

Verified `/isolinux` contents include:

- `boot.cat`
- `isolinux.bin`
- `isolinux.cfg`
- `live.cfg`
- `menu.cfg`
- `stdmenu.cfg`
- `utilities.cfg`
- `splash.png`
- Syslinux modules such as `menu.c32`, `vesamenu.c32`, `chain.c32`, `hdt.c32`, `ldlinux.c32`, `libcom32.c32`, `libgpl.c32`, `libmenu.c32`, `libutil.c32`

Implementation consequence:

The first FX Live remaster can preserve the original LMDE boot equipment and replace the live root filesystem at `/live/filesystem.squashfs`. Kernel and initrd are already clearly located under `/live/`. Before modifying boot menus, inspect the exact contents of GRUB and Syslinux configuration files and the UEFI image. Do not guess the boot arguments or menu include chain.

Status: source image structure verified; no remastering performed yet.
