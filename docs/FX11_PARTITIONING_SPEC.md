# FX11 Partitioning Specification

Status: implementation baseline for FX11 Installer.

This specification defines how FX11 should partition disks before Windows installation. It follows Microsoft's current Windows 11 UEFI/GPT deployment guidance while preserving FX11's core principle: **Your System. Your Rules.**

## Decision

FX11 partitioning is handled by the **FX11 Installer before standard Windows Setup**.

The user never has to leave the FX11 partitioning experience merely because they choose an advanced layout. FX11 owns all three modes:

1. **FX11 only** — guided automatic layout.
2. **FX11 + Other OS** — guided automatic multi-OS layout.
3. **Custom / advanced** — fully user-controlled layout inside FX11 Installer.

Standard Windows Setup is launched only after the FX11 partitioning stage has finished or the user explicitly chooses to continue with an already prepared layout.

Legacy BIOS/MBR is not part of the normal FX11 layout. If support is added later, it should be a separate advanced path rather than silently changing the partition scheme.

## Microsoft layout followed by FX11

For a normal UEFI/GPT deployment, the recommended Windows side of the disk uses this order:

`EFI System | MSR | FX11 / Windows | Windows Recovery`

For **FX11 + Other OS**, the reserved space is placed after Windows Recovery:

`EFI System | MSR | FX11 / Windows | Windows Recovery | unallocated — Other OS`

The Other OS area is not formatted by FX11.

## Partition sizes used by guided modes

### EFI System Partition

FX11 guided mode uses **300 MiB FAT32**.

Rationale:

- large enough for supported UEFI/GPT Windows deployment,
- suitable for both 512/512e and 4Kn media,
- leaves additional room for future boot-manager entries in multi-OS systems.

The ESP receives a temporary drive letter only while FX11 Installer is preparing the system. It should not retain a normal drive letter after installation.

### Microsoft Reserved partition

**16 MiB**, no filesystem and no user drive letter.

### FX11 / Windows partition

NTFS.

In **FX11 only**, it receives all usable space remaining after EFI, MSR and Recovery.

In **FX11 + Other OS**, the user chooses the size of FX11 / Windows. The remaining tail of the disk becomes unallocated Other OS space.

FX11's product-level minimum for a guided Windows partition is initially **64 GiB**. This is an FX11 usability guardrail, not a claim that 64 GiB is Microsoft's universal minimum for every Windows edition or workload.

### Windows Recovery

NTFS, using the Windows Recovery GPT type:

`DE94BBA4-06D1-4D40-A16A-BFD50179D6AC`

and the appropriate hidden/required GPT attributes.

The partition should be sized from the actual Windows image being deployed:

`winre.wim + FX11 WinRE customizations + at least 250 MiB free`

FX11 additionally uses a **1024 MiB minimum floor** in guided mode.

The installer must not assume `winre.wim` is always the same size. The required size should be measured from the selected Windows image.

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

## Custom / advanced mode

Custom mode is **not** a hand-off to the stock Windows partition screen. It remains inside FX11 Installer.

The goal is to give an advanced user full control while continuously explaining what FX11 needs.

The custom editor should expose the selected physical disk as a graphical partition map and table. The user can:

- create partitions,
- delete partitions,
- resize partitions where the underlying storage operation supports it safely,
- format supported filesystems,
- leave areas unallocated,
- choose the target partition for FX11,
- select or create an EFI System Partition,
- select or create a Windows Recovery partition,
- preserve existing partitions,
- preserve another installed operating system,
- work with multiple physical disks,
- choose an existing compatible ESP rather than create a new one when appropriate,
- intentionally build a non-standard arrangement after acknowledging warnings.

FX11 should not artificially restrict an advanced user to the guided layout when Windows can technically be installed on the selected arrangement.

### Required information shown in Custom mode

FX11 must continuously distinguish between:

- **Required for this installation** — items without which FX11/Windows cannot proceed in the selected boot mode,
- **Recommended by FX11** — the layout FX11 prefers for serviceability and recovery,
- **Optional / user choice** — data partitions, Other OS space and other user-defined structures,
- **Unsupported / invalid** — arrangements Windows Setup or the selected firmware mode cannot use.

For normal UEFI/GPT installation, the interface should explain that FX11 expects:

- an EFI System Partition on the selected boot disk,
- an MSR where required for the Windows GPT layout,
- an NTFS partition large enough for FX11 / Windows,
- a Recovery partition strongly recommended for WinRE and servicing.

The user may deviate from the recommended arrangement where technically possible, but the UI must explain the consequence before allowing continuation.

Examples:

- no Recovery partition: **allowed only if the final deployment path can support that choice**, but clearly marked as not recommended because WinRE/recovery functionality will be reduced;
- using an existing ESP: allowed if it is valid and has enough free space;
- preserving an existing Linux/BSD partition: allowed; FX11 must not reformat it unless explicitly instructed;
- leaving additional unallocated space: allowed;
- creating extra NTFS data partitions: allowed;
- using another physical disk for data or Other OS: allowed;
- trying to install UEFI Windows without a usable ESP: blocked until corrected.

### Custom-mode safety model

Custom mode gives more control, not less safety.

Every pending action should be staged first and shown as a plan. No disk change is committed immediately when the user clicks create/delete/resize.

The final review must show, per physical disk:

- current layout,
- proposed layout,
- partitions to be created,
- partitions to be deleted,
- partitions to be resized,
- partitions to be formatted,
- partitions preserved unchanged,
- selected FX11 target,
- selected ESP,
- selected Recovery partition,
- any unallocated space,
- any warnings or reduced-functionality choices.

Only after explicit confirmation should FX11 apply the queued operations.

## Safety model for all modes

No destructive operation may run until the user has seen and confirmed:

- disk number,
- manufacturer/model,
- capacity,
- current partition summary,
- proposed new partition map,
- exact FX11 and Other OS sizes where applicable,
- all deletions/formats/resizes,
- a clear warning describing what data will be lost.

FX11 must never assume Disk 0 is correct.

In guided clean-layout modes, the sequence is conceptually:

1. `select disk N`
2. `clean`
3. `convert gpt`
4. create EFI
5. create MSR
6. create FX11 / Windows
7. create Windows Recovery
8. stop, leaving remaining space unallocated in Other OS mode

In Custom mode, FX11 instead generates an explicit operation plan from the user's choices. A whole-disk `clean` is used only when the user has explicitly chosen an action equivalent to erasing the disk.

The Linux-side Builder never executes DiskPart or modifies physical disks. Actual disk enumeration and changes occur only in the Windows PE FX11 Installer environment.

## Installation continuation

After partitioning succeeds, FX11 Installer should continue directly with the prepared Windows target rather than forcing the user to identify the same partition again.

The final deployment path must:

- apply the selected Windows image to the chosen FX11 partition,
- install UEFI boot files to the ESP chosen in FX11 Installer,
- deploy/configure WinRE when a Recovery partition is part of the chosen layout,
- register the selected Recovery environment correctly,
- never place FX11 boot files on another physical disk merely because another ESP is already present,
- preserve every partition that the confirmed plan marked as unchanged.

## Implementation model

`src/fx11/partitioning.py` contains the non-destructive planning layer.

Guided layout planning can already be unit-tested on Linux. The next implementation step is to extend the planning model so Custom mode contains explicit user-defined partition operations instead of being represented as an empty/no-op layout.

Actual disk enumeration, graphical editing, explicit confirmation and partition execution belong to the Windows PE FX11 Installer layer and must first be tested against disposable QEMU virtual disks.
