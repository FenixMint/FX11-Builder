# 2026-09-13 — FX11 boot UX preview before integration

User request: do not integrate a new GRUB visual theme into the Builder until the proposed design has first been reviewed visually.

## Current technical status

The refreshed test3 hybrid image is structurally valid:
- focused media-boot tests passed;
- GPT + protective MBR present;
- EFI boot partition present;
- BIOS and UEFI El Torito entries preserved;
- refreshed FX11 media grub.cfg staged;
- physical runtime validation of test3 is still pending.

## UX requirements from first physical boot

The installation-media GRUB must not look like a raw black technical GRUB screen. It should have a finished product-level presentation inspired by the clarity of Linux Mint's boot theme, while retaining a distinct FX11 identity.

Desired direction:
- dark branded FX11 background;
- visible FX11 / FX logo treatment;
- simple vertical menu with a clear selected row;
- minimal on-screen text;
- no developer wording in user-facing entries;
- consistent visual language between installation-media GRUB and the later installed FX Boot Manager;
- avoid technical clutter and avoid over-design.

Current proposed installation-media entries for visual preview:
1. FX Partition Manager
2. FX11 Installer
3. UEFI Firmware Settings

`powered by GParted` should be shown as attribution/subtext rather than making the main menu label long.

## Implementation rule

No theme assets or theme integration are approved yet. First produce a visual mockup. After user approval, implement the GRUB theme within actual GRUB capabilities and test it in QEMU and on physical USB.
