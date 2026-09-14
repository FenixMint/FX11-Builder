# FX Base audit: LMDE 7 vs Linux Mint 22.3

Date: 2026-09-14
Status: architectural direction / package audit

## Decision

FX Live for the FX11 installation flow will be developed on an LMDE 7 / Debian 13 foundation rather than on GParted Live.

Work done to create FX Live should also be treated as the beginning of a reusable FX Linux foundation, but FX11 and FX Linux remain separate products. FX11-Builder contains only the FX11-specific installer and the shared live-base work required by it; a dedicated FX Linux project/repository can be split out when the shared base becomes independently useful.

The intended layering is:

- FX Base: LMDE 7 / Debian 13 derived core, Mint Cinnamon/XApps where useful, FX branding and system adjustments.
- FX Live: reduced live profile built from FX Base, autostarts FX11 Installer and provides disk, network, firmware and repair tools.
- FX Linux: future full desktop profile built from the same FX Base.

Do not mix Ubuntu Noble repositories directly into LMDE/Debian. When a component from Ubuntu-based Mint is useful, prefer one of:

1. Debian native equivalent,
2. Debian backports,
3. source-level port/rebuild against Debian,
4. FX replacement implementation.

## Package/function audit

Linux Mint 22.3 (Zena) and LMDE 7 (Gigi) share most of the Mint user-space stack. The Mint package repositories list matching/current versions of core tools such as mintinstall, mintupdate, mintlocale, mintreport, mintstick, mintsysadm, mintsystem, mintwelcome, themes/icons, Cinnamon/XApps and related desktop components.

The important functional differences for FX are concentrated in a relatively small set:

### 1. Driver Manager

Linux Mint 22.3 ships `mintdrivers`; LMDE does not. Mint documents that mintdrivers depends on the Ubuntu `ubuntu-drivers` backend and therefore is not available in LMDE.

FX relevance: HIGH.

Do not import the Ubuntu binary stack directly. Prototype an `FX Drivers` layer using Debian-native information and packages. Useful Debian building blocks include `nvidia-detect`, Debian non-free/non-free-firmware packages, DKMS packages such as `broadcom-sta-dkms`, modalias/lspci/udev inspection and Debian backports firmware.

The existing Mint mintdrivers UI/source may be studied for UX and, subject to licence review, may be adapted to a Debian backend rather than `ubuntu-drivers`.

### 2. NVIDIA / hybrid graphics integration

Linux Mint 22.3 provides `nvidia-prime-applet`; it is not part of the LMDE 7 Mint package set.

FX relevance: MEDIUM for FX Linux, LOW for the first FX11 Live installer.

Debian provides `switcheroo-control` and NVIDIA packages. FX can later provide its own simple hybrid-GPU status/switching UX if required instead of importing Ubuntu PRIME infrastructure wholesale.

### 3. Installer stack

Linux Mint 22.3 uses Mint's Ubuntu-based Ubiquity stack and `ubiquity-slideshow-mint`.
LMDE 7 ships `live-installer` and `mint-live-session` instead.

FX relevance: HIGH as architectural reference, but neither installer is to be used as the Windows installation engine.

The Mint/Ubiquity integrated partitioning UX remains an important design reference for FX11 Installer. LMDE live session is the more relevant runtime foundation.

### 4. System-adjustment packages

Linux Mint 22.3 uses `ubuntu-system-adjustments`.
LMDE 7 uses `debian-system-adjustments`.

FX relevance: HIGH.

Use the Debian/LMDE adjustments as the base and introduce a separate FX adjustment layer rather than copying Ubuntu-specific assumptions.

### 5. Kernel / HWE / firmware

Ubuntu-based Mint has a polished HWE path and HWE ISOs. As of 2026-09, Mint 22.3 offers regular/HWE kernel tracks including newer kernels for recent hardware.

This is a useful model, but not a reason to import Ubuntu packages. Debian 13 backports already provides a very recent kernel and newer firmware packages. FX Base should use a controlled stable + backports policy for hardware enablement.

Potential policy:

- stable Debian kernel as compatibility fallback;
- current tested trixie-backports kernel for FX Live / newer hardware;
- firmware from trixie-backports where it materially improves hardware support;
- preserve a tested fallback kernel in installed FX Linux.

### 6. Mint tools parity

LMDE 7 already contains the majority of the desktop features users associate with Mint, including Cinnamon, XApps and Mint tools. Therefore the gap between Ubuntu-based Mint and LMDE is much smaller than the difference between plain Debian and Mint.

This supports LMDE as the preferred FX foundation.

### 7. Controlled imports are already part of LMDE practice

The LMDE repository itself contains an `import` section for selected software originating outside the Debian base (for example app-install data and Boot Repair related packages). This reinforces the policy that selective, explicit imports/rebuilds are acceptable, while wholesale Ubuntu-repository mixing is not.

## Initial FX package priorities

P0 — required for FX11 Live foundation:

- LMDE live-session functionality
- Cinnamon/GTK runtime needed by FX11 Installer
- NetworkManager and normal hardware/network stack
- GParted as advanced/custom partitioning tool
- `parted`, `sgdisk`, filesystem tools
- udev/lspci/lsblk/blkid/smart tools needed for detection and validation
- NTFS/FAT tooling
- current firmware set
- controlled backports kernel option
- FX autostart/session wrapper

P1 — useful shared FX Base functionality:

- FX Drivers prototype replacing the missing LMDE Driver Manager function
- NVIDIA detection via Debian-native tools
- Broadcom and non-free-firmware detection/install guidance
- hardware diagnostics/reporting
- boot repair/recovery helpers where they fit the FX model

P2 — primarily future FX Linux:

- hybrid-GPU applet/switching UX
- full desktop application selection
- update-channel/continuous-release UX
- end-user recovery/snapshot integration

## Release/update model

LMDE itself is not rolling release. FX should nevertheless investigate a continuous-release user experience on top of a stable LMDE/Debian base:

- stable base ABI and system components;
- regular FX package updates;
- Mint desktop updates where compatible;
- tested kernel/firmware updates from backports;
- periodically refreshed installation/live images rather than a forced six-month product-release cadence.

This is intended to reduce maintenance churn while avoiding the risk of making the installer platform depend on a full Debian Testing/Sid rolling base.

## Next validation

Before the first FX Live implementation, produce an exact installed-package comparison between current Linux Mint 22.3 Cinnamon and LMDE 7 Cinnamon (ISO manifests or equivalent) and classify differences as:

- needed by FX Live,
- useful for future FX Linux,
- Ubuntu-specific and replaceable,
- irrelevant.

Then build the first minimal LMDE-derived FX Live prototype with FX11 Installer autostart and GParted available only as the advanced/custom partition editor.
