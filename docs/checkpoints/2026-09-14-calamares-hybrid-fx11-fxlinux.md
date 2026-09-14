# Calamares hybrid FX11 / FX Linux direction — 2026-09-14

Status: architecture research checkpoint. Not implemented or physically validated yet.

## Goal

Use one LMDE/Debian-based FX Live environment as the common first-stage platform for both:

- FX11 installation,
- future FX Linux installation.

The preferred product direction is a single hybrid installation image built around one FX Live userspace rather than two unrelated live images.

## Calamares findings

Calamares is a modular installer framework. Its top-level `settings.conf` defines an ordered sequence of visible view modules and execution jobs. Branding and module configuration can be supplied without patching Calamares core. Custom view modules are supported as Qt/C++ plugins; custom job modules may be implemented in Python. Modules share structured state through Global Storage.

The stock partition module uses KPMCore, the same storage library used by KDE Partition Manager. It already supports manual and automated partitioning, GPT partition type GUIDs, unformatted partitions and custom partition layouts.

Important limitation for FX11: the stock manual partition page is Linux-oriented and only enables continuation when a root (`/`) mount point exists. Therefore it should not be treated as a drop-in Windows partition UI. Using a fake `/` mount point for the Windows NTFS partition would be a prototype hack, not the desired architecture.

## Recommended architecture

Do not fork Calamares core unless later proven necessary. Keep upstream Calamares and add FX-owned configuration and modules.

Use two installation profiles sharing the same Calamares binary and branding family:

1. FX Linux profile
   - standard Calamares Linux flow,
   - stock or lightly configured Calamares/KPMCore partition module,
   - install LMDE-derived FX Linux,
   - desktop choice planned separately: Cinnamon, MATE, KDE, TDE.

2. FX11 profile
   - shared language / keyboard / UX where practical,
   - FX-specific Windows partition view based on Calamares/KPMCore concepts rather than pretending Windows NTFS is Linux root,
   - Windows layout semantics: ESP + MSR + Windows + Recovery,
   - custom FX11 job writes deterministic install context including install_id and GPT GUID identifiers,
   - reboot into WinPE,
   - WinPE phase performs DISM /Apply-Image, BCDBoot, WinRE and FX11 provisioning.

Calamares supports alternate configuration directories (`-c` for testing and XDG-based configuration lookup), so separate FX11 and FX Linux sequences can be maintained without duplicating the whole installer framework. Production packaging should use stable wrapper/config paths rather than relying on test-only invocation conventions.

## Hybrid image concept

Prefer one FX Live kernel/initrd/root filesystem with multiple boot modes instead of embedding two complete Linux ISOs.

Proposed GRUB UX:

1. Install FX11
2. Install FX Linux
3. Try FX Linux / Tools
4. UEFI Firmware Settings

The first three Linux entries may boot the same kernel/initrd/squashfs while passing an FX mode parameter. The live startup service then launches the corresponding installer profile or desktop/tools mode.

For FX11, the same medium also contains the prepared WinPE boot environment and the Windows payload produced from the user's own Windows ISO. After Linux-stage validation the machine reboots and the medium enters WinPE phase 2 using the saved installation context.

The previously observed physical failures of direct Microsoft EFI chainloading from ISO9660 still apply. The self-contained FAT WinPE boot environment remains a relevant technical direction and should be validated independently; this checkpoint does not claim that handoff works yet.

## Distribution / licensing model

A public FX Linux / FX Live image may contain only redistributable Linux components.

A combined FX11 + FX Linux hybrid image containing Microsoft Windows binaries must be generated locally by FX11 Builder from user-supplied Windows installation media; do not publish such generated Windows images.

## Why this is preferable

- one coherent FX installer UX,
- integrated partitioning instead of launching GParted as the main installer,
- no special GParted-to-installer handoff icon,
- shared live platform and branding,
- Calamares remains useful for FX Linux,
- KPMCore/storage work can be reused for the Windows-specific partition UI,
- FX11 and FX Linux remain separate products while sharing an FX Base / FX Live foundation.

## Next validation

Before implementation, prototype the following in isolation:

- LMDE-based FX Live boots to Cinnamon and can autostart a small FX launcher,
- Calamares can run two independent FX configuration profiles from the same live system,
- stock Calamares Linux partition flow works on LMDE base,
- minimal custom FX11 view/job module can read disks and exchange state through Global Storage,
- KPMCore can create the required Windows GPT types (ESP, MSR, Basic Data, Recovery) without Linux-root assumptions,
- phase-1 context survives reboot and WinPE can resolve target partitions by GUID/markers,
- WinPE boot from the combined medium is physically validated.
