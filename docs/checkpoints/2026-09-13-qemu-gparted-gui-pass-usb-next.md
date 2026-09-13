# Checkpoint — QEMU GParted GUI reached; next: physical USB boot

Date: 2026-09-13

Observed on the low-end HP test host:

- QEMU/OVMF booted the genuine FX11 Home test ISO.
- FX GRUB successfully took over the UEFI boot path.
- The default `FX Partition Manager — powered by GParted` path launched GParted Live.
- GParted Live reached the graphical GParted application.
- The VM was stopped before completing a partition layout because the HP host was too slow for a comfortable full installation test.

This is stronger runtime evidence than the previous checkpoint: the path `OVMF -> FX GRUB -> GParted Live -> GParted GUI` is now observed working.

Next milestone: write the current FX11 ISO to a physical USB device and test real firmware boot. Raw block-copy USB bootability of the rebuilt ISO has not yet been proven, so the first USB write is explicitly a test, not a supported/released USB claim.

Safety rule for USB testing:

- never guess the target device name;
- identify the removable device with `lsblk`/`udevadm` first;
- unmount all mounted partitions on that device;
- write only to the whole device (for example `/dev/sdX`, not `/dev/sdX1`);
- verify the selected device model/size immediately before writing.
