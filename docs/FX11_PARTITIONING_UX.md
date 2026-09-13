# FX11 Installer — Partitioning UX

This document defines the user-facing partitioning flow for FX11 Installer.

The goal is simple: partitioning should be understandable for beginners and unrestricted enough for advanced users, while destructive operations must never be ambiguous.

## Core rule

Before changing a disk, FX11 must explain:

1. which physical disk will be modified,
2. what the selected layout will create,
3. how much space FX11 will receive,
4. how much space will remain for another operating system when a multi-OS layout is selected,
5. whether existing partitions and files will be deleted,
6. what FX11 requires versus what it merely recommends,
7. what will happen after confirmation.

The installer must show the final planned layout before making any destructive change.

## Step 1 — Choose the physical disk

User-facing heading:

**Where do you want to install FX11?**

Introductory text:

> Select the physical disk that should contain FX11. The selected disk may be repartitioned in the next step. Other detected disks will not be modified unless you explicitly choose them in Custom mode.

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

### Option B — FX11 + Other OS

Suggested label:

**FX11 + Other OS — reserve space for another operating system**

Description:

> Choose this option if you want FX11 and another operating system on the same computer. FX11 will automatically create the Windows partitions and reserve the selected part of the disk for the other operating system.

#### What does “Other OS” mean?

**Other OS** means another operating system installed alongside FX11. The installer should explain this by family instead of presenting one flat list.

**Linux**  
Examples used by FX11: **Linux Mint, Fedora, openSUSE, Rocky Linux, AlmaLinux, Debian and Arch Linux**.

**BSD**  
Examples used by FX11: **FreeBSD, OpenBSD and NetBSD**.

**Other Unix / Unix-like systems**  
This category may include other compatible Unix or Unix-like operating systems where their installer, boot method and hardware support allow coexistence with Windows 11 on the same machine. Examples may include **illumos-based systems such as OmniOS or OpenIndiana**, where technically appropriate.

**Other operating systems**  
The reserved area is intentionally generic and may also be used by a different compatible operating system outside the Linux/BSD/Unix-like families. FX11 must not imply guaranteed compatibility; the system's installer, UEFI support, Secure Boot behavior, hardware drivers and boot manager determine whether a particular OS can actually be installed successfully.

FX11 documentation and user-facing examples should use the Linux distributions listed above when examples are needed. Ubuntu is intentionally not part of the FX11 example/recommendation list.

> FX11 does not assume what the second operating system will be. It therefore does not create Linux-specific filesystems, swap, `/home`, BSD disk structures or any other OS-specific partitions. The reserved **Other OS** area remains unallocated so that the installer of the chosen operating system can create the layout it actually needs.

Compatibility note:

> Reserving disk space does not guarantee that every operating system will install or coexist correctly with Windows 11. Hardware support, UEFI, Secure Boot, disk encryption and boot-manager behavior depend on the selected operating system. FX11 should explain these considerations in the post-installation Multi-OS Guide.

The user should be able to set:

- size for FX11,
- size reserved for Other OS,
- preferably through both a slider and exact size fields.

The slider and graphical disk bar must use the labels:

**FX11** ↔ **Other OS**

Example visual plan:

`EFI | MSR | FX11 350 GB | Recovery | 600 GB unallocated — Other OS`

The UI should clearly distinguish **unallocated — Other OS** from a formatted Windows partition.

Destructive warning when applicable:

> Existing partitions and files on the selected disk will be removed before this new layout is created.

### Option C — Custom / advanced

Suggested label:

**Custom — build your own disk layout**

Description:

> Full control over the disk layout. Create, delete, resize, preserve and format partitions inside FX11 Installer. FX11 will explain what Windows needs and what FX11 recommends, but you decide the final arrangement.

This option remains entirely inside **FX11 Installer**. The user is not pushed into the stock Windows partitioning screen merely because they chose an advanced layout.

Custom mode should show:

- a graphical disk map,
- a partition table,
- filesystem/type,
- size,
- used/free space when detectable,
- detected operating system or role when identification is reliable,
- flags such as EFI System, MSR, Windows, Recovery, data or unallocated.

Available actions should include, where technically supported:

- **Create partition**,
- **Delete partition**,
- **Resize partition**,
- **Format partition**,
- **Leave unallocated**,
- **Preserve unchanged**,
- **Use as FX11**,
- **Use as EFI System Partition**,
- **Use as Recovery**.

For multiple-disk systems, Custom mode may also let the user inspect and intentionally modify another physical disk, but FX11 must never make that choice automatically.

## Guidance inside Custom mode

The key UX rule is that the interface must explain the difference between **required**, **recommended** and **optional**.

Suggested status chips:

- **Required for FX11**
- **Recommended by FX11**
- **Optional**
- **Existing / preserved**
- **Warning**
- **Invalid for this installation**

For normal UEFI/GPT installation, an information panel should say:

**What does FX11 need?**

- **EFI System Partition** — required for UEFI boot. FX11 can create one or use a compatible existing ESP.
- **Microsoft Reserved (MSR)** — part of the normal Windows GPT layout.
- **FX11 / Windows** — NTFS partition used for Windows and FX11.
- **Windows Recovery** — strongly recommended for WinRE, repair and servicing. The user may see the consequence before choosing a layout without it where technically supported.

The user should never have to memorize Windows partitioning rules. FX11 should continuously validate the layout and tell them what is missing or unusual.

Examples of messages:

> **EFI System Partition missing.** FX11 cannot boot in UEFI mode without a usable ESP. Create one or select an existing compatible ESP.

> **Recovery partition not selected.** FX11 recommends a Recovery partition so Windows Recovery Environment remains available. You can continue without it only if this installation path supports that choice.

> **Existing Linux partition detected.** This partition will be preserved unless you explicitly delete, resize or format it.

> **Existing ESP selected.** FX11 will add its boot files to this EFI System Partition and preserve existing boot entries where possible.

> **Unallocated space will remain after installation.** You can use it later for another operating system or data partition.

## Staged changes — nothing happens immediately

Custom partition editing should work like a transaction.

Clicking **Delete**, **Create**, **Resize** or **Format** changes only the proposed layout on screen. The actual disk is untouched until the final review and confirmation.

The interface should visually distinguish:

- current partitions,
- newly created partitions,
- partitions scheduled for deletion,
- partitions scheduled for resize,
- partitions scheduled for format,
- partitions preserved unchanged,
- unallocated space.

An **Undo** action should be available before commit.

## Step 3 — Explain the Windows partitions

The preview screen should let the user expand a small **What are these partitions?** explanation.

### EFI System Partition

> A small FAT32 system partition used by UEFI firmware to start Windows and other operating systems. It normally has no drive letter and should not be used for personal files.

### Microsoft Reserved (MSR)

> A small technical partition used internally by Windows on GPT disks. It normally contains no user files and does not receive a drive letter.

### FX11 / Windows

> The main Windows partition. FX11, installed applications and most user data are stored here unless the user later chooses another location.

### Recovery

> Contains Windows recovery tools used for troubleshooting and repair. FX11 recommends keeping a supported Recovery layout instead of removing it simply to save a small amount of disk space.

### Unallocated — Other OS

> Disk space intentionally left unused by Windows and reserved for another operating system. Linux, BSD, another Unix-like system or another compatible OS can later use this area and create the partitions and filesystems it requires.

## Step 4 — Final review before partitioning

User-facing heading:

**Review the disk layout**

The screen must show, for every disk affected:

- disk model and capacity,
- current layout,
- proposed layout,
- exact sizes,
- partitions to be deleted,
- partitions to be created,
- partitions to be resized,
- partitions to be formatted,
- partitions preserved unchanged,
- FX11 target partition,
- selected EFI System Partition,
- selected Recovery partition,
- remaining unallocated space,
- plain-language consequences.

Example automatic summary:

**Target:** Disk 0 — Samsung SSD 990 PRO — 1 TB  
**Mode:** FX11 + Other OS  
**FX11:** 350 GB  
**Other OS:** approximately 600 GB unallocated  
**Action:** The current partition layout on Disk 0 will be removed and replaced with the layout shown above. No other physical disk will be modified automatically.

Example Custom summary:

**Disk 0 — Samsung SSD 990 PRO — 1 TB**  
- Preserve existing EFI System Partition — 300 MB  
- Preserve Linux partition — 220 GB  
- Delete old Windows partition — 300 GB  
- Create FX11 / Windows — 450 GB NTFS  
- Create Windows Recovery — 1 GB NTFS  
- Leave 29 GB unallocated  

FX11 should state exactly which operations are destructive.

## Destructive confirmation

The main action must not simply say `Next`.

For a whole-disk replacement:

**Erase selected disk and create this layout**

For Custom mode:

**Apply these partition changes**

Immediately above the button:

> This operation will apply the partition changes listed above. Deleted or formatted partitions may permanently lose their files. Check the physical disk model, capacity and every destructive action before continuing.

FX11 should require an explicit confirmation checkbox such as:

**I have reviewed the listed disk changes and understand which partitions may lose data.**

Only after this confirmation should the destructive action become available.

## Multiple-disk systems

If more than one physical disk is detected, FX11 must make this obvious.

Suggested notice:

> Multiple physical disks were detected. Guided modes modify only the selected target disk. Custom mode can modify additional disks only when you explicitly select and edit them.

FX11 must never automatically choose another disk because it appears empty, is listed first by firmware or has a particular disk number.

## Existing operating systems

If an existing Windows, Linux, BSD, Unix-like or other operating-system installation is detected, the installer should identify it where reliable.

Suggested warning:

> An existing operating-system installation appears to be present. It will be preserved unless the proposed layout explicitly deletes, formats or overwrites its partitions.

Detection is advisory only; if identification is uncertain, FX11 should describe the existing partitions rather than guess which operating system they contain.

## Recommended default

For a new/empty machine, FX11 should visually mark **FX11 only** as the simplest default.

It must not preselect a destructive action in a way that allows the user to erase a disk through repeated `Next` clicks without reviewing the final layout.

For multi-OS users, the UI should emphasize that **FX11 + Other OS reserves space but does not install the second operating system**.

Custom mode should be presented as **full control with guidance**, not as a dangerous hidden expert option.

## After partitioning

Once the selected layout has been created successfully, FX11 Installer should continue to Windows installation without asking the user to manually select the partitions that FX11 just created or selected.

FX11 passes the chosen Windows target, ESP and Recovery configuration into the deployment stage.

For the FX11 + Other OS mode, the installer should remember that the machine was prepared for another operating system so that FX11 Control Center can later show a non-intrusive **Multi-OS Guide** explaining the next steps for Linux, BSD, Unix-like and other compatible operating systems.

This guide must not imply that WSL2 is required. WSL2 remains an entirely separate, optional feature that can be installed later from FX11 First Run or FX11 Control Center.
