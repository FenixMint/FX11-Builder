# FX11 Automatic Partitioning Specification

Status: implementation baseline for FX11 Installer.

This specification defines how FX11 should partition a disk in automatic modes. It follows Microsoft's current Windows 11 UEFI/GPT deployment guidance while preserving FX11's multi-OS principle: **Your System. Your Rules.**

## Decision

FX11 automatic partitioning will target **UEFI + GPT** systems.

Automatic modes:

1. **FX11 only**
2. **FX11 + Other OS**
3. **Custom / advanced** — no automatic destructive partitioning

Legacy BIOS/MBR is not part of the automatic FX11 layout. If support is added later, it should be a separate advanced path rather than silently changing the partition scheme.

## Microsoft layout followed by FX11

For UEFI/GPT deployment, the automatic Windows side of the disk uses this order:

`EFI System | MSR | FX11 / Windows | Windows Recovery`

Microsoft's current guidance places the Windows Recovery partition immediately after the Windows partition so Windows can service, resize and recreate WinRE when necessary.

For **FX11 + Other OS**, the reserved space is placed after Windows Recovery:

`EFI System | MSR | FX11 / Windows | Windows Recovery | unallocated — Other OS`

This ordering is deliberate. The Other OS area is not a Windows data partition and is not formatted by FX11.

## Partition sizes

### EFI System Partition

FX11 automatic mode uses **300 MiB FAT32**.

Rationale:

- Microsoft currently documents a minimum of 200 MB for 512-byte/512e sector media,
- Microsoft documents a minimum of 300 MB for 4Kn media,
- using 300 MiB avoids a separate automatic-layout branch for sector size while remaining comfortably within the supported model.

The ESP receives a temporary drive letter only while FX11 Installer is preparing the system. It should not keep a normal Windows drive letter after installation.

### Microsoft Reserved partition

**16 MiB**, no filesystem and no user drive letter.

### FX11 / Windows partition

NTFS.

In **FX11 only**, it receives all usable space remaining after EFI, MSR and Recovery.

In **FX11 + Other OS**, the user chooses the size of FX11 / Windows. The remaining tail of the disk becomes unallocated Other OS space.

FX11's product-level minimum for an automatically created Windows partition is initially **64 GiB**. This is an FX11 usability guardrail, not a claim that 64 GiB is Microsoft's universal minimum for every Windows edition or workload. The value may be raised after real-image testing.

### Windows Recovery

NTFS, with Windows Recovery GPT type:

`DE94BBA4-06D1-4D40-A16A-BFD50179D6AC`

and hidden/required GPT attributes appropriate to a Windows Recovery partition.

The partition should be sized from the actual Windows image being deployed:

`winre.wim + FX11 WinRE customizations + at least 250 MiB free`

FX11 additionally uses a **1024 MiB minimum floor** for its automatic layout. Microsoft's documentation currently recommends 990 MB as a practical minimum for custom deployment layouts; FX11 rounds that floor upward to 1 GiB.

The builder/installer must not assume that `winre.wim` is always the same size. The size should be measured from the selected Windows image when the installer pipeline is finalized.

## FX11 + Other OS

The user-facing slider is:

**FX11** ↔ **Other OS**

FX11 creates only the Windows-required partitions. The Other OS portion remains **unallocated**.

FX11 must not create or guess:

- ext4,
- Btrfs,
- XFS,
- swap,
- `/home`,
- ZFS,
- UFS,
- BSD disklabels,
- illumos/Unix-specific structures,
- any other second-OS filesystem or partition layout.

The later operating-system installer owns that decision.

User-facing examples can be grouped as:

- **Linux:** Linux Mint, Fedora, openSUSE, Rocky Linux, AlmaLinux, Debian, Arch Linux,
- **BSD:** FreeBSD, OpenBSD, NetBSD,
- **Other Unix / Unix-like:** e.g. suitable illumos-family systems where hardware/boot support allows it,
- **Other compatible systems:** anything capable of coexisting with the machine's UEFI/GPT configuration.

Reserving space does not guarantee that every operating system supports the machine, Secure Boot configuration, storage controller or chosen boot-manager arrangement.

## Safety model

No destructive operation may run until the user has seen and confirmed:

- disk number,
- manufacturer/model,
- capacity,
- current partition summary,
- proposed new partition map,
- exact FX11 and Other OS sizes,
- a clear erase/repartition warning.

The automatic DiskPart script must be generated only after a specific physical disk has been selected. FX11 must never assume Disk 0 is correct.

For automatic clean layouts, the sequence is conceptually:

1. `select disk N`
2. `clean`
3. `convert gpt`
4. create EFI
5. create MSR
6. create FX11 / Windows
7. create Windows Recovery
8. stop, leaving remaining space unallocated in Other OS mode

The generated script is a deployment artifact; the Linux-side Builder never executes DiskPart.

## Custom / advanced mode

Custom mode is intentionally non-destructive from FX11's automatic-layout engine.

It must not generate or run a clean-disk DiskPart script. Instead it hands control to the manual/advanced partition-selection path so the user can preserve an existing operating system, use prepared free space or handle unusual multi-disk arrangements.

## Installation continuation

After automatic partitioning succeeds, FX11 Installer should continue directly with the prepared Windows target rather than forcing the user to identify the same partition again.

The final deployment path must also:

- apply the selected Windows image to the FX11 partition,
- install UEFI boot files to the selected disk's ESP,
- deploy/configure WinRE on the Recovery partition,
- confirm that the Recovery partition is correctly registered,
- never place FX11 boot files on another physical disk merely because another ESP is already present.

## Implementation model now present in the repository

`src/fx11/partitioning.py` contains the non-destructive planning layer and DiskPart-script generator.

The planning layer can be unit-tested on Linux without touching a disk. Actual disk enumeration, explicit confirmation and DiskPart execution belong to the future Windows PE installer layer and must first be tested against disposable QEMU virtual disks.
