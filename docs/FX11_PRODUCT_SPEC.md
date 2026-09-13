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
5. offers optional application installation,
6. explains why each offered application may be useful,
7. downloads the current vendor release at install time instead of shipping stale installers inside the ISO,
8. allows the user to skip all optional software.

No optional third-party application is installed silently without user consent.

## Recommended application catalogue

### Browsers

- **LibreWolf** — Firefox-based browser focused on privacy, reduced telemetry and hardened defaults.
- **Firefox** — mainstream open-source browser with broad compatibility and extension support.
- **DuckDuckGo Browser** — privacy-focused browser with tracker blocking and simple privacy controls.
- **Brave** — Chromium-based browser with built-in tracker/ad blocking and strong site compatibility.
- **Thorium** — Chromium-based browser focused on performance and responsiveness.
- **SRWare Iron** — Chromium-based browser positioned around reducing Google-specific tracking and integration.

### Mail

- **Thunderbird** — open-source desktop email client with support for multiple providers and local mail workflows.

### Archives

- **7-Zip** — lightweight open-source archive utility with excellent 7z support.
- **PeaZip** — graphical archive manager with broad format support and additional archive/security tools.

### Drivers

- **Driver Booster** — optional driver discovery/update utility.
- This item must be clearly marked as optional and should never replace Windows Update or OEM driver channels automatically.

## Application installation policy

- FX11 should resolve/download the latest stable release from an official vendor source or trusted package source at the time of installation.
- Installers are not permanently embedded in the base ISO unless a later offline profile explicitly requests this.
- The catalogue stores metadata, source URL/resolver, checksum/signature policy, silent-install arguments and uninstall information.
- Failed downloads must not block first login.
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
- optional app recommendations and installs,
- privacy explanation,
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
