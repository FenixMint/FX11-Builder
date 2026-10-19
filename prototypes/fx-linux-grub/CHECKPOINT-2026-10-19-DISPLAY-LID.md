# ThinFedora / FX11 dual-boot display checkpoint — 2026-10-19

## Context

Reference machine:

- Lenovo ThinkPad L13 Gen 2 AMD
- Fedora 44 COSMIC / ThinFedora
- FX11 / Windows 11 in dual boot
- external monitor: Ancor Communications Inc VW225, 1680x1050
- physical connection: HDMI from laptop -> DVI at monitor
- internal display: AU Optronics 1920x1080 eDP panel
- test also performed while running on battery with the lid closed

This note belongs to the temporary FX Linux/GRUB prototype area inside FX11-Builder. It documents Linux-side behavior that matters on the same dual-boot reference machine. It is **not** an FX11 Windows configuration change.

## Problem observed

After selecting Fedora in GRUB:

1. the external monitor could lose signal / enter standby before the COSMIC greeter;
2. after entering the login password, the machine could suspend again;
3. COSMIC Night Light did not always appear to apply reliably.

The second symptom initially looked like a monitor issue, but logs proved that the **whole laptop entered suspend** immediately after the greeter -> user-session handoff.

## DRM / output discovery

Kernel DRM connectors on the reference machine:

```text
card1-DP-1: disconnected
card1-DP-2: disconnected
card1-eDP-1: connected
card1-HDMI-A-1: connected
```

The external VW225 is `HDMI-A-1`.
The internal panel is `eDP-1`.
The DP connectors correspond to DisplayPort capability exposed through USB-C, not to the HDMI-connected monitor.

## COSMIC output-state issue

COSMIC stores display state in:

```text
~/.local/state/cosmic-comp/outputs.ron
```

The problematic combined HDMI + eDP profile had the external monitor enabled but positioned at:

```text
position: (1920, 0)
xwayland_primary: false
```

while the internal eDP panel was disabled at position `(0, 0)`.

That left the only active display offset from the origin and not marked primary.

A backup was created:

```text
~/.local/state/cosmic-comp/outputs.ron.bak
```

The combined HDMI + eDP profile was corrected so the external monitor is:

```text
position: (0, 0)
enabled: true
xwayland_primary: true
```

while the internal eDP panel remains disabled for the closed-lid external-monitor scenario.

### Result

After reboot:

- GRUB -> COSMIC greeter no longer caused the external monitor to fall asleep.

## Lid / suspend issue

The remaining failure after login was traced to `systemd-logind`.

Boot logs showed the sequence:

```text
systemd-logind: Suspending...
New session of user fenix
Starting systemd-suspend.service
PM: suspend entry (s2idle)
```

The ThinkPad sleep LED also confirmed the machine itself was sleeping.

No custom effective lid policy was present before the fix.

A drop-in was added:

```text
/etc/systemd/logind.conf.d/90-thinfedora-lid.conf
```

with:

```ini
[Login]
HandleLidSwitch=suspend
HandleLidSwitchExternalPower=ignore
HandleLidSwitchDocked=ignore
```

Intent:

- normal standalone-laptop behavior may still suspend on lid close;
- external-monitor / docked behavior must not suspend merely because the lid is closed;
- this must also work while on battery, not only on AC power.

### Result

Test after reboot with:

- HDMI external monitor connected,
- lid closed,
- laptop running on battery,

was successful:

- monitor stayed active through boot and greeter;
- login no longer triggered system suspend;
- COSMIC session started normally.

## Night Light

The Flatpak COSMIC Night Light autostart service did start during the tested session.
On the successful post-fix reboot, Night Light applied automatically.

Earlier logs also showed that forcing the privileged Night Light helper can temporarily disturb DRM ownership / mode-setting. This remains a reason to treat the future Fenix Night Light implementation separately from the display-state and lid-policy fixes.

## FX11 relevance

The Windows/FX11 GRUB entry remained present throughout these tests.

These fixes are **Linux-side only** and should not be interpreted as Windows/FX11 configuration requirements.
For the future split into dedicated FX Linux and FX11 repositories:

- keep the GRUB dual-boot compatibility notes in shared boot documentation;
- move `outputs.ron` / COSMIC / `logind` behavior into FX Linux machine-profile documentation;
- preserve the FX11 Windows entry and class mapping unchanged.

## Verified state at stop

Working combination on the reference machine:

- FX OS GRUB active;
- Fedora BLS preserved;
- FX11 / Windows Boot Manager preserved;
- UEFI Firmware Settings preserved;
- external HDMI-DVI monitor stable from GRUB through COSMIC greeter;
- no suspend after login with closed lid + external monitor;
- successful test while on battery;
- Night Light started automatically.

This is the known-good reference state before further GRUB cosmetics or Plymouth branding work.
