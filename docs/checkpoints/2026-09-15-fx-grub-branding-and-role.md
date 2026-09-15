# FX GRUB branding and role decision — 2026-09-15

## Decision
The bootloader presented to the user on FX media should be visibly branded as **FX**, not as stock LMDE or generic GRUB.

This is primarily a product/UX layer over upstream GRUB. Do not fork GRUB core unless later testing proves that a core patch is actually necessary.

## Media boot menu
For the future FX Live / hybrid medium, GRUB should present product-neutral FX branding and entries such as:

- Install FX11
- Install FX Linux
- Try FX Linux / Tools
- UEFI Firmware Settings

The first three Linux entries may boot the same LMDE-derived live kernel/initrd and pass a mode selector such as:

- `fx.mode=windows`
- `fx.mode=linux`
- `fx.mode=live`

## Branding direction
Use the already-approved FX visual direction: dark teal/black background, mountain/fjord/night/aurora feel, large FX identity, clean menu, teal/green accent, public author label `Fenix`.

Remove LMDE-specific product wording from the visible primary menu on FX media, while retaining honest upstream provenance in documentation/about/legal areas.

## Technical principle
Keep upstream GRUB where practical:

- reuse the LMDE boot stack and UEFI/BIOS compatibility where possible,
- replace/own `grub.cfg`, theme assets, labels, timeout behavior and FX-specific kernel parameters,
- avoid unnecessary GRUB-core changes,
- keep fallbacks/recovery entries available.

## Important separation
Installation-media FX GRUB and the future installed-system **FX Boot Manager** are related visually but are separate responsibilities:

1. **FX Media GRUB** — boots FX Live and routes into FX11 / FX Linux / tools.
2. **FX Boot Manager** — installed on target disk later and manages installed operating systems.

Do not conflate the two implementations.

## Status
Architecture decision only. No ISO has been modified yet.
