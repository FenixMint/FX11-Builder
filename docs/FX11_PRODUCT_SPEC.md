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
7. downloads the current vendor release at install time instead of shipping stale installers inside the ISO,
8. allows the user to skip optional third-party software.

No optional third-party application is installed silently without user consent.

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

### Archives

- **7-Zip** — lightweight open-source archive utility with excellent 7z support.
- **PeaZip** — graphical archive manager with broad format support and additional archive/security tools.

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
- build and validate bootable ISO.

### FX11 First Run
Runs after normal Windows OOBE and first interactive user sign-in.

Responsibilities:
- user-facing personalization,
- taskbar/Start selection,
- recommended browser selection,
- optional app recommendations and installs,
- privacy explanation,
- verification/installation of mandatory compatibility runtimes,
- creation of the user's chosen FX11 desktop setup.

### FX11 Control Center
Persistent configuration application available after First Run.

Planned sections:
- Appearance,
- Start & Taskbar,
- Applications,
- Privacy,
- Windows,
- Updates,
- FX11 Status.

## Product principle

**FX11 gives the user choices instead of silently making permanent choices for them.**

The base system can provide opinionated defaults, but user-facing shell, applications and privacy options must remain understandable, reversible and configurable after installation.
