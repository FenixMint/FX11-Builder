# FX OS GRUB checkpoint — 2026-10-04

## Status

First real boot test: **successful**.

The FX OS theme loaded on the reference ThinFedora machine and GRUB remained functional.

## What was verified on hardware

- FX OS background loaded correctly.
- Fedora BootLoaderSpec entries remained present.
- Current Fedora kernel remained bootable.
- Older Fedora kernel remained present.
- Fedora rescue entry remained present.
- Windows Boot Manager remained present.
- UEFI Firmware Settings remained present.
- Fedora class icon was rendered.
- Windows class icon was rendered.
- `grub2-script-check /boot/grub2/grub.cfg` returned no errors.
- generated `grub.cfg` contains:
  - FX OS theme,
  - `blscfg`,
  - Windows entry,
  - UEFI firmware entry.

## Current machine configuration

```text
GRUB_THEME="/boot/grub2/themes/fxos/theme.txt"
GRUB_GFXMODE="1920x1080,1680x1050,auto"
```

Working theme directory:

```text
/boot/grub2/themes/fxos/
```

Rollback assets remain available:

```text
/boot/grub2/themes/breeze/
/etc/default/grub.fxos-backup
```

## Current fonts

Created locally from static Droid Sans TTF files:

```text
fxos-regular-24.pf2
fxos-bold-28.pf2
```

with internal names:

```text
FXOS Regular
FXOS Bold
```

## Current icons

The icons are intentionally FX-branded rather than stock Fedora/Windows artwork.

- `fedora.png`: **FX Linux Hat** — penguin wearing an FX hat.
- `windows.png`: **FX 11** — a window looking out onto the world / space.

GRUB class mapping:

```text
grub_class fedora  -> icons/fedora.png
--class windows    -> icons/windows.png
```

## Current visual issues

The first boot proved the mechanism, but the theme is not final.

1. The large dark menu rectangle is still inherited from Breeze through:
   `menu_pixmap_style = "roundedsquare_*.png"`.
2. The desired FX names are not yet applied. GRUB still shows Fedora BLS titles and the stock Windows Boot Manager title.
3. UEFI Firmware Settings has no dedicated FX icon yet.
4. Selected-item styling still needs the intended subtle FX-blue/glass treatment.
5. Font appearance must be checked again after the PF2 internal-name rebuild.
6. The current screenshots were taken on the external 20-inch 1680x1050 monitor; the internal 13-inch 1920x1080 panel still needs a real readability test.

## Naming policy

Do **not** manually edit generated `grub.cfg`.

Desired primary names:

```text
FX Linux Fedora
FX 11
UEFI Firmware Settings
```

Fedora names must survive kernel updates. A future FX Linux implementation should use a persistent generation/hook mechanism, likely around BLS/`kernel-install`, rather than changing each generated entry by hand.

Older kernels and rescue must remain discoverable.

## Boot branding layers

Current boot sequence:

1. Lenovo UEFI firmware splash — leave untouched to avoid firmware risk.
2. FX OS GRUB — active prototype and safe to refine.
3. Fedora Plymouth/BGRT splash — later replace with an FX OS Plymouth theme.
4. COSMIC session.

Decision: **do not modify the first Lenovo UEFI splash**. The post-GRUB Plymouth splash is the next branding target after GRUB is complete.

## Next GRUB work

- replace Breeze menu pixmaps with FX-specific selected/normal assets,
- remove or greatly reduce the opaque dark menu block,
- add dedicated UEFI icon,
- implement persistent FX Linux / FX 11 naming,
- retest on the internal 13-inch display,
- preserve Fedora BLS, rescue, Windows and UEFI behavior throughout.

## Binary assets currently validated locally

These exact files were used/prepared locally and are not yet committed as binaries on this staging branch:

```text
fxos-grub-background.png
SHA256 cd06a7f64c654ca47e2a5c7879418d0e881ef50b9b221215b9803bc4f39ecc95

fedora.png
SHA256 b07395a0c6990252fe4b45e82b43589d5043231ea97ac52bb6978991acc8a14d

windows.png
SHA256 9011edce08035aed6e8e57d419706309100815051b6cb9a66347aeace4fb40ea
```

Binary artwork should be committed when the FX Linux repository is created or when the final GRUB asset set is frozen.
