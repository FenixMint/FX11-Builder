# FX11 Product Specification

## Identity

- Product name: **FX11 OS**
- Tagline: **FX11 OS for you**
- Supporting line: **Your System. Your Rules.**
- The Start button uses the **FX** mark only.
- FX11 has its own logo, wallpaper set, installer branding, first-run branding and control-center branding.

## Default desktop experience

- Default wallpaper: FX11 "Lazur" — based on the tropical Windows XP-style Azure/Lazur aesthetic: turquoise water, small island, palms, bright blue sky and sailboat.
- Default taskbar style: Windows XP-inspired.
- Default taskbar position: **top of the screen**.
- The taskbar position remains user-configurable later: top, bottom, left or right where the selected shell implementation supports it.
- Start menu styles are user-selectable: XP, Windows 7, Windows 10 or Windows 11.
- Start menu and taskbar choices are changeable after installation in **FX11 Control Center**.

## Windows account creation

FX11 must not create or embed a permanent user account.

- User creation stays in the normal Windows OOBE flow.
- No hard-coded user name such as User, Admin, FX11 or developer-specific names may be baked into the ISO.
- FX11 First Run starts only after the user has completed normal Windows OOBE and signed in to the newly created account.
- User-specific settings are applied to the current account at that point.
- System-wide defaults may be staged in the Default User profile, but this must never create an account.

## FX11 First Run

On the first normal desktop sign-in, FX11 launches **FX11 First Run**.

The first-run experience:

1. welcomes the user to FX11,
2. explains the default privacy posture,
3. confirms/changes Start menu style,
4. confirms/changes taskbar position,
5. offers recommended browser and application installation,
6. explains why each offered application may be useful,
7. offers privacy and Proton tools,
8. offers **optional** WSL2 setup with Linux distribution selection,
9. downloads the current vendor release at install time instead of shipping stale installers inside the ISO,
10. allows the user to skip optional third-party software and WSL2.

No optional third-party application or WSL2 feature is installed or enabled silently without user consent.

## Recommended application catalogue

### Browsers

Browser choice is a core part of the FX11 privacy model. FX11 should strongly recommend privacy-respecting browsers at First Run and explain the differences in plain language.

- **LibreWolf** — Firefox-based browser focused on privacy, reduced telemetry and hardened defaults.
- **Firefox** — mainstream open-source browser with broad compatibility and extension support.
- **DuckDuckGo Browser** — privacy-focused browser with tracker blocking and simple privacy controls.
- **Brave** — Chromium-based browser with built-in tracker/ad blocking and strong site compatibility.
- **Thorium** — Chromium-based browser focused on performance and responsiveness.
- **SRWare Iron** — Chromium-based browser positioned around reducing Google-specific tracking and integration.

FX11 does **not** recommend or preinstall Google Chrome because its default Google account, advertising and telemetry ecosystem does not align with the privacy-first goals of FX11. However, FX11 must not technically block a user from installing Chrome later: **Your System. Your Rules.**

FX11 First Run should encourage the user to choose at least one browser from the recommended list before finishing setup and should clearly identify privacy-oriented choices.

### Mail

- **Thunderbird** — open-source desktop email client with support for multiple providers and local mail workflows.

### Office and documents

- **LibreOffice** — strongly recommended open-source office suite and the preferred FX11 office package.
- FX11 should explain that LibreOffice is actively developed, works locally, supports common Microsoft Office formats and does not require a cloud account for normal use.
- **Apache OpenOffice** is not part of the recommended FX11 catalogue because LibreOffice is the preferred actively developed open-source office suite.

### PDF tools

- **SumatraPDF** — lightweight, fast open-source reader for PDF and other document formats.
- **PDFsam Basic** — open-source local PDF utility for merging, splitting, extracting and rotating pages.
- **LibreOffice Draw** — useful for opening and making basic edits to many PDF files as part of LibreOffice.
- **Stirling-PDF** — advanced optional PDF toolkit for users who need a broader feature set such as conversion, OCR, redaction and document operations. It should be presented as an advanced/local-tool option rather than a mandatory component.

### Archives

- **7-Zip** — lightweight open-source archive utility with excellent 7z support.
- **PeaZip** — graphical archive manager with broad format support and additional archive/security tools.

### Privacy and Proton tools

FX11 should offer a dedicated **Privacy & Security** section with Proton tools as recommended privacy-oriented services.

- **Proton VPN** — optional encrypted VPN client for protecting network traffic, especially on untrusted networks.
- **Proton Pass** — optional password manager for passwords, passkeys, 2FA workflows and aliases.
- **Proton Drive** — optional encrypted cloud-storage client and privacy-oriented alternative to OneDrive/Google Drive.
- **Proton Mail / Calendar** — present as privacy-oriented communication services, while clearly explaining when desktop or premium functionality depends on the user's Proton plan.
- Proton tools remain optional; FX11 should explain what each does before installation and must not create accounts on the user's behalf.

### Drivers and important system components

- **Driver Booster** — optional driver discovery/update utility that can help the user find current device drivers and important driver-related components after installation.
- FX11 First Run should explain that Driver Booster may be useful especially on hardware where Windows Update does not immediately provide the newest or most complete driver set.
- Driver Booster remains optional and must not silently override Windows Update or OEM driver channels.

### Mandatory compatibility runtimes

The current supported Microsoft Visual C++ Redistributables are treated as **mandatory FX11 compatibility components**, not optional applications.

- **Microsoft Visual C++ Redistributable x86** — install the current supported Microsoft runtime for 32-bit applications.
- **Microsoft Visual C++ Redistributable x64** — install the current supported Microsoft runtime for 64-bit applications.
- On 64-bit Windows, both x86 and x64 packages are installed because many Windows applications remain 32-bit and require the x86 runtime.
- FX11 should verify whether the current supported runtimes are already present and install/update them automatically when required.
- These packages must come from Microsoft or an official Microsoft package source.

## Linux in FX11

FX11 should actively support users who want Linux tools without forcing them to abandon Windows.

### WSL2

WSL2 is an **optional add-on**, not part of the mandatory FX11 base installation.

FX11 First Run and FX11 Control Center may offer an optional **Linux / WSL2** module. If the user does not select it, the required WSL/virtualization Windows features must remain untouched by FX11.

The WSL2 installation flow must be designed specifically to avoid the default Ubuntu installation path. FX11 must **never** execute a bare `wsl --install` command as its normal setup action, because Microsoft currently uses that command to install WSL together with Ubuntu by default.

The FX11 flow should instead:

1. enable/install the WSL platform **without installing a Linux distribution**, using the supported no-distribution path where available,
2. query the live WSL catalogue with `wsl --list --online` / `wsl -l -o`,
3. display the distributions that are actually available at that moment,
4. mark **Fedora, Debian and AlmaLinux** as FX11-recommended choices when they appear in the live catalogue,
5. keep every other available distribution visible and selectable,
6. install only the exact distribution explicitly chosen by the user, using its returned WSL distribution name,
7. avoid launching or setting a distribution as default until the user has explicitly selected it.

Ubuntu must not be promoted, preselected or automatically installed by FX11. If Ubuntu appears in the live WSL catalogue, it may remain visible as an ordinary user-selectable option because **Your System. Your Rules.**

The module should also:

- explain in plain language what WSL2 is and when it is useful,
- offer to enable the required Windows features only after explicit user selection,
- allow installation to be skipped and revisited later,
- include a short getting-started guide after installation,
- provide basic commands for updating packages, accessing Windows files, launching Linux shells and shutting down/restarting WSL,
- include notes for developers about Git, SSH, Python, containers and command-line tooling where appropriate,
- avoid hard-coding the complete distro list; the live Microsoft WSL catalogue is the source of truth for what can be installed through the standard WSL path.

If a desired distribution is not present in the online WSL catalogue, FX11 may later expose an **Advanced / Import distribution** workflow based on supported WSL import mechanisms, but this must be separate from the simple First Run path.

### Installer disk layout and automatic partitioning

Disk layout is a **pre-installation installer decision**. FX11 Installer must present partitioning choices before Windows is installed and must be able to create the selected layout automatically.

The installer should offer at least these modes:

- **FX11 — entire disk** — automatically prepare the selected target disk for a standard UEFI/GPT Windows 11 installation and allocate the remaining usable space to Windows.
- **FX11 + Other OS** — automatically prepare the Windows-required partitions, create the FX11/Windows partition at the selected size, and leave the chosen remainder of the disk **unallocated** for another operating system.
- **Custom / advanced** — do not apply an automatic layout; hand control to an advanced partition-selection flow for users who need an existing or unusual disk layout.

**Other OS** means another operating system installed alongside FX11. User-facing examples should be grouped by family:

- **Linux:** Linux Mint, Fedora, openSUSE, Rocky Linux, AlmaLinux, Debian, Arch Linux.
- **BSD:** FreeBSD, OpenBSD, NetBSD.
- **Other Unix / Unix-like:** compatible systems from other Unix or Unix-like families, including illumos-based systems such as OmniOS or OpenIndiana where technically appropriate.
- **Other operating systems:** any other compatible OS whose installer, UEFI support, Secure Boot behavior, hardware support and boot manager allow coexistence with FX11.

Ubuntu is not part of FX11's example/recommendation list.

For the FX11 + Other OS automatic mode the user must be able to choose the amount of disk space allocated to **FX11** versus **Other OS**, preferably by both a visual slider and exact size fields. The slider labels must be:

**FX11** ↔ **Other OS**

FX11 must not assume what the second operating system is. It should not create ext4, Btrfs, swap, `/home`, BSD-specific partitions or any other OS-specific layout. The **Other OS** area remains unallocated so the installer of the selected operating system can create the filesystems and partitions it actually requires.

Before any destructive automatic partitioning, FX11 Installer must:

1. clearly identify the target physical disk by model, capacity and disk number,
2. show the proposed partition layout and resulting FX11/Other OS space,
3. warn that existing partitions/data on the selected target disk will be removed when the chosen mode requires a clean-disk layout,
4. require a separate explicit confirmation,
5. never automatically modify another detected disk,
6. stop rather than guess if disk identity or layout is ambiguous.

The automatic UEFI/GPT layout must preserve the partitions required for a supported Windows installation, including EFI/system and Windows recovery/servicing requirements. Exact sizes and layout rules should be generated from the supported Windows installation model rather than hard-coded blindly.

A typical user-facing flow should therefore be:

**Where do you want to install FX11?** -> choose physical disk -> **Choose disk layout** -> `FX11 only` / `FX11 + Other OS` / `Custom` -> choose FX11/Other OS space if applicable -> review graphical partition plan -> confirm destructive changes -> automatic partitioning -> Windows installation.

Multi-OS setup itself is completed later by installing the selected second operating system into the reserved unallocated space. FX11 Control Center may provide a post-installation **Multi-OS Guide**, but partition planning belongs to the installer, not First Run.

## Application installation policy

- FX11 should resolve/download the latest stable release from an official vendor source or trusted package source at the time of installation.
- Mandatory Microsoft Visual C++ Redistributables are installed or updated automatically as compatibility components.
- Optional third-party applications remain user-selectable.
- Installers are not permanently embedded in the base ISO unless a later offline profile explicitly requests this.
- The catalogue stores metadata, source URL/resolver, checksum/signature policy, silent-install arguments and uninstall information.
- Failed optional downloads must not block first login.
- The user can return to the same catalogue later from FX11 Control Center.

## Privacy baseline

FX11 defaults to strong privacy settings while preserving core Windows functionality.

Disable or restrict by default:

- optional diagnostic/telemetry collection,
- Windows Error Reporting uploads,
- feedback prompts and Feedback Hub integration where removable,
- CEIP/customer experience tasks,
- Activity History publishing/upload,
- Advertising ID,
- tailored experiences,
- consumer-content suggestions and sponsored recommendations,
- unnecessary telemetry-related scheduled tasks and services where this can be done without damaging servicing.

Preserve:

- Windows Update,
- Windows activation,
- Microsoft Defender and security intelligence updates,
- Microsoft Store unless a user-selected profile removes it,
- core networking and servicing infrastructure.

FX11 Control Center must include a **Privacy Check / Restore FX11 Privacy** action to detect settings that Windows Update may have changed and re-apply the selected FX11 privacy profile.

## Components

### FX11 Builder
Linux-side ISO creation tool.

Responsibilities:
- inspect Microsoft Windows 11 media,
- select edition,
- inject FX11 assets and provisioning,
- stage First Run and Control Center,
- apply machine-wide privacy baseline safely,
- stage the FX11 installer partitioning flow and automatic disk-layout logic,
- build and validate bootable ISO.

### FX11 Installer
Pre-installation environment responsible for disk and installation choices.

Responsibilities:
- identify available physical disks,
- let the user select the target disk,
- offer standard, FX11 + Other OS and custom partitioning modes,
- preview the proposed disk layout,
- perform confirmed automatic partitioning,
- leave Other OS space unallocated in the multi-OS mode,
- continue into the Windows installation using the prepared FX11/Windows target.

### FX11 First Run
Runs after normal Windows OOBE and first interactive user sign-in.

Responsibilities:
- user-facing personalization,
- taskbar/Start selection,
- recommended browser selection,
- optional app recommendations and installs,
- privacy explanation,
- verification/installation of mandatory compatibility runtimes,
- optional WSL2 setup and distribution selection,
- creation of the user's chosen FX11 desktop setup.

### FX11 Control Center
Persistent configuration application available after First Run.

Planned sections:
- Appearance,
- Start & Taskbar,
- Applications,
- Privacy,
- Linux / WSL2,
- Multi-OS Guide,
- Windows,
- Updates,
- FX11 Status.

## Product principle

**FX11 gives the user choices instead of silently making permanent choices for them.**

The base system can provide opinionated defaults, but user-facing shell, applications, Linux integration and privacy options must remain understandable, reversible and configurable after installation.
