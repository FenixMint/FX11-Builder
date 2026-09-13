# Checkpoint — hybrid USB partition layout visible on physical pendrive

Date: 2026-09-13

After writing the hybrid-repacked FX11 ISO to the Kingston DataTraveler 3.0 pendrive, Linux exposes a GPT-derived partition layout that was not visible with the previous non-hybrid ISO.

Observed with `lsblk -p -o NAME,MODEL,SIZE,TRAN,RM,FSTYPE,LABEL,MOUNTPOINTS`:

- `/dev/sdb` — DataTraveler 3.0, 57.6G, USB, removable, `iso9660`, label `FX11`
- `/dev/sdb1` — ~718K, no filesystem reported
- `/dev/sdb2` — 16M, `vfat`, label `FX11BOOT`
- `/dev/sdb3` — ~7.8G, no filesystem reported

Interpretation:

- the 16 MiB FAT partition corresponds to the EFI System Partition exposed by the hybrid build;
- the small and large additional partitions correspond to the GPT layout/gaps created around the embedded EFI boot image and ISO payload;
- this is expected for the new hybrid image and is materially different from the previous raw ISO, which showed only a single ISO9660 device and no loaded System Area/GPT.

Next step: physical UEFI boot test from the same USB port, with Secure Boot disabled for the current unsigned FX GRUB development payload.
