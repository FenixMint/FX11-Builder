# FX11 Installer — Partitioning UX

This document defines the user-facing partitioning flow for FX11 Installer.

The goal is simple: automatic partitioning should be easy to understand, while destructive operations must never be ambiguous.

## Core rule

Before changing a disk, FX11 must explain:

1. which physical disk will be modified,
2. what the selected layout will create,
3. how much space FX11 will receive,
4. how much space will remain for Linux when dual boot is selected,
5. whether existing partitions and files will be deleted,
6. what will happen after confirmation.

The installer must show the final planned layout before making any destructive change.

## Step 1 — Choose the physical disk

User-facing heading:

**Where do you want to install FX11?**

Introductory text:

> Select the physical disk that should contain FX11. The selected disk may be repartitioned in the next step. Other detected disks will not be modified automatically.

Each disk card should show at least:

- disk number,
- manufacturer/model,
- total capacity,
- connection/type when available, for example NVMe, SATA or USB,
- current partition/use summary,
- a warning if the disk contains existing partitions or data.

Example:

**Disk 0 — Samsung SSD 990 PRO 1 TB — NVMe**  
Existing partitions detected. Selecting an automatic clean-install layout will erase the existing partition table and data on this disk.

FX11 must not identify disks only as `Disk 0` or `Disk 1`; model and capacity must always be visible.

## Step 2 — Choose the disk layout

User-facing heading:

**How should FX11 use this disk?**

### Option A — FX11 only

Suggested label:

**FX11 only — use the disk for Windows**

Description:

> Recommended when this computer will use FX11 as its only operating system. FX11 will automatically create the partitions required by Windows 11 and use the available disk space for the Windows installation.

Short explanation:

- easiest option,
- automatic UEFI/GPT layout,
- creates the system, Windows and recovery partitions required for the supported installation,
- no space is intentionally reserved for another operating system.

Destructive warning when applicable:

> Existing partitions and files on the selected disk will be removed.

### Option B — FX11 + Linux

Suggested label:

**FX11 + Linux — prepare the disk for dual boot**

Description:

> Choose this option if you want to install Linux next to FX11. FX11 will automatically create the Windows partitions and reserve part of the disk for Linux.

Important explanation:

> FX11 does not create Linux partitions. The Linux area will remain unallocated. When you later run the installer of your chosen Linux distribution, it can use that free space and create its own filesystem, swap and other partitions according to that distribution's requirements.

Why this is safer:

> Different Linux distributions use different partition layouts and filesystems. Leaving the Linux area unallocated avoids forcing an unsuitable layout before the Linux distribution has been chosen.

The user should be able to set:

- size for FX11,
- size reserved for Linux,
- preferably through both a slider and exact size fields.

Example visual plan:

`EFI | MSR | FX11 350 GB | Recovery | 600 GB unallocated for Linux`

The UI should clearly distinguish **unallocated for Linux** from a formatted Windows partition.

Destructive warning when applicable:

> Existing partitions and files on the selected disk will be removed before this new layout is created.

### Option C — Custom / advanced

Suggested label:

**Custom — choose partitions manually**

Description:

> For experienced users, existing multi-disk systems and unusual disk layouts. FX11 will not automatically erase or repartition the disk. You choose where Windows should be installed.

Additional note:

> Use this option if you need to preserve existing partitions, install FX11 into already prepared free space, or manage the disk layout yourself.

FX11 should not present this option as dangerous; it is simply an advanced/manual path.

## Step 3 — Explain the Windows partitions

The preview screen should let the user expand a small **What are these partitions?** explanation.

Suggested text:

### EFI System Partition

> A small system partition used by UEFI firmware to start Windows and other operating systems. It normally has no drive letter and should not be used for personal files.

### Microsoft Reserved (MSR)

> A small technical partition used internally by Windows on GPT disks. It normally contains no user files and does not receive a drive letter.

### FX11 / Windows

> The main Windows partition. FX11, installed applications and most user data are stored here unless the user later chooses another location.

### Recovery

> Contains Windows recovery tools used for troubleshooting and repair. FX11 keeps a supported Windows recovery layout instead of removing this partition to save a small amount of disk space.

### Unallocated for Linux

> Disk space intentionally left unused by Windows. It is reserved for a later Linux installation. The Linux installer can turn this area into the partitions and filesystems it needs.

## Step 4 — Final review before partitioning

User-facing heading:

**Review the disk layout**

The screen must show:

- selected physical disk,
- disk model and capacity,
- selected mode,
- graphical partition bar,
- exact sizes,
- whether existing data will be deleted,
- a plain-language description of what happens after confirmation.

Example summary:

**Target:** Disk 0 — Samsung SSD 990 PRO — 1 TB  
**Mode:** FX11 + Linux  
**FX11:** 350 GB  
**Linux:** approximately 600 GB unallocated  
**Action:** The current partition layout on Disk 0 will be removed and replaced with the layout shown above. No other physical disk will be modified automatically.

## Destructive confirmation

The main action must not simply say `Next`.

Suggested button text:

**Erase selected disk and create this layout**

For layouts that do not erase the whole disk, use wording matching the actual operation instead.

Immediately above the button:

> This operation changes disk partitions and may permanently remove existing files from the selected disk. Make sure important data has been backed up and confirm that the disk model and capacity shown above are correct.

FX11 should require an explicit confirmation checkbox such as:

**I understand that the selected disk will be repartitioned and existing data on it may be permanently deleted.**

Only after this confirmation should the destructive action become available.

## Multiple-disk systems

If more than one physical disk is detected, FX11 must make this obvious.

Suggested notice:

> Multiple physical disks were detected. FX11 will modify only the disk selected below. Check the model and capacity carefully before continuing.

The installer must never automatically choose another disk because it appears empty, is listed first by firmware or has a particular disk number.

## Existing operating systems

If an existing Windows or Linux installation is detected on the selected disk, the installer should say so where detection is reliable.

Suggested warning:

> An existing operating-system installation appears to be present on this disk. Choosing an automatic clean-install layout will remove its partitions. Choose **Custom** if you intend to preserve the existing installation.

Detection is advisory only; if identification is uncertain, FX11 should describe the existing partitions rather than guess which operating system they contain.

## Recommended default

For a new/empty machine, FX11 should visually mark **FX11 only** as the simplest default.

It must not preselect a destructive action in a way that allows the user to erase a disk through repeated `Next` clicks without reviewing the final layout.

For dual-boot users, the UI should emphasize that **FX11 + Linux prepares the space but does not install Linux**.

## After partitioning

Once the selected layout has been created successfully, the installer can continue to Windows installation without asking the user to manually select the partitions that FX11 just created.

For the dual-boot mode, the installer should remember that the machine was prepared for Linux so that FX11 Control Center can later show a non-intrusive **Dual Boot Guide** explaining the next steps.

This guide must not imply that WSL2 is required. WSL2 remains an entirely separate, optional feature that can be installed later from FX11 First Run or FX11 Control Center.
