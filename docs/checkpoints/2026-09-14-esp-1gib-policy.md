# ESP sizing policy — 1 GiB default

Date: 2026-09-14

## Decision

For new FX-managed GPT layouts, the default EFI System Partition (ESP) size is **1 GiB**.

The design goal is to prefer **one shared ESP per system disk** rather than creating additional small ESPs for each installed OS.

## Rationale

A 1 GiB ESP gives comfortable headroom for:

- Microsoft Windows boot files and BCD,
- FX Boot Manager / GRUB assets,
- FX Linux boot files,
- future kernels / initramfs / UKI-style boot artifacts if used,
- recovery and maintenance boot assets,
- dual-boot or multi-boot layouts,
- future expansion without repartitioning the start of the disk.

Small ESPs (for example 100–300 MiB) can become restrictive on multi-OS systems and may lead installers or users to create additional ESPs later. Multiple ESPs are technically possible, but FX should avoid them when one correctly-sized shared ESP is practical.

## Fresh-disk target layout

- ESP: 1 GiB, FAT32, GPT type EFI System Partition
- MSR: 16 MiB
- OS partitions as required (FX11 / FX Linux)
- Recovery partition as required

## Existing systems

FX Installer must not blindly create a second ESP.

Preferred order:

1. detect the existing ESP and inspect its size / free space,
2. reuse it when it has sufficient headroom,
3. if it is too small, offer a safe enlargement when the partition map allows it,
4. create another ESP only when reuse or safe enlargement is not practical.

Exact minimum free-space thresholds for reusing an existing ESP remain to be validated during implementation and physical testing.

## Architecture impact

The planned Calamares/KPMCore-based FX partitioning module should implement this policy for both FX11 and future FX Linux / dual-boot layouts.
