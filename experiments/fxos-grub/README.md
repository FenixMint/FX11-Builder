# FX OS GRUB theme prototype

> Temporary home: this work is intentionally kept on a separate branch of **FX11-Builder** and is expected to be extracted into a dedicated FX Linux / FX OS repository later.

## Purpose

Build a complete, maintainable GRUB theme for the FX family rather than a one-off wallpaper hack.

The target visual identity is **FX OS** with two primary user-facing system names:

- **FX Linux Fedora**
- **FX 11**

The actual boot menu remains real GRUB UI rendered over the background image. Menu labels, icons and selection state are not baked into the wallpaper.

## Reference machine

Current validation target:

- Lenovo ThinkPad L13 Gen 2
- internal display: 13-inch, 1920×1080
- frequently used external display: 20-inch, 1680×1050
- Fedora Linux 44 COSMIC
- UEFI
- Fedora BLS boot entries

The 13-inch panel is the readability baseline. The theme must remain comfortable there and still look good on the external monitor.

## Design contract

The implementation follows the proven Linux Mint GRUB-theme model:

- complete theme directory,
- separate `theme.txt`,
- separate `background.png`,
- real `icons/` directory,
- icons selected from GRUB entry classes,
- no hand-editing generated `grub.cfg`,
- Fedora BLS entries remain BLS-managed,
- preserve all recovery/older-kernel/firmware entries,
- keep a known-good theme as rollback.

Expected target layout:

```text
/boot/grub2/themes/fxos/
├── theme.txt
├── background.png
├── icons/
│   ├── fedora.png
│   ├── windows.png
│   ├── os.png
│   └── firmware.png
├── menu_*.png
├── selected_*.png
└── *.pf2
```

## Confirmed GRUB classes

### Fedora

Fedora entries are BLS-generated and currently contain:

```text
grub_class fedora
```

Therefore Fedora-family icons should be provided as:

```text
icons/fedora.png
```

This automatically covers current and future Fedora kernel entries as long as BLS retains the `fedora` class.

### Windows / FX 11

The detected Windows entry is generated with:

```text
--class windows --class os
```

Therefore the primary Windows-family icon is:

```text
icons/windows.png
```

## Entries that must remain available

Do not remove or hide boot choices merely to make the first screen prettier.

The prototype must preserve:

- current Fedora kernel,
- older Fedora kernel entries,
- Fedora rescue entry,
- Windows Boot Manager / future **FX 11** label,
- **UEFI Firmware Settings**.

A future polished layout may visually prioritize FX Linux Fedora and FX 11 while still keeping the remaining entries directly accessible.

## Target naming

User-facing target names:

```text
FX Linux Fedora
FX 11
```

Persistent naming must be implemented at the source/configuration layer. Do not rename generated `/boot/grub2/grub.cfg` lines manually because regeneration would discard those changes.

## Readability

The original Breeze-derived theme used 14/16-point fonts and ~33 px menu rows, which were too small for a 13-inch 1080p display.

FX OS baseline should use approximately:

- icons: 48–56 px displayed size,
- menu rows: 56–64 px,
- menu text: roughly 24–28 px-equivalent GRUB font sizing,
- stronger selected-row contrast,
- percentage-based placement where practical.

A separate HiDPI/2K profile can be introduced later, following the same idea as Linux Mint's normal and 2K variants.

## Background

The selected art direction uses the FX OS planetary horizon / mountain / reflective-lake image with cool blue and warm amber light.

Important: the boot-entry UI shown in visual mockups is only a design reference. The production `background.png` must contain only the artwork/branding, while GRUB renders the actual menu.

## Safety / rollback

Current known-good theme:

```text
/boot/grub2/themes/breeze/theme.txt
```

Prototype theme:

```text
/boot/grub2/themes/fxos/theme.txt
```

Do not overwrite the Breeze directory.

Before activating the final prototype:

1. retain Breeze unchanged,
2. validate that all files referenced by `theme.txt` exist,
3. generate GRUB configuration normally,
4. verify all Fedora BLS, rescue, Windows and UEFI entries remain present,
5. reboot-test on the internal ThinkPad panel,
6. test again with the external monitor.

## Current ThinFedora prototype state

The working machine currently has:

```text
GRUB_THEME="/boot/grub2/themes/breeze/theme.txt"
```

and a separate `/boot/grub2/themes/fxos/` directory cloned from Breeze for development.

The prototype `theme.txt` already references:

```text
desktop-image: "background.png"
```

Activation is intentionally deferred until the FX OS theme has its final menu sizing and icons.

## Next steps

1. Create original **FX Linux Fedora** icon as `icons/fedora.png`.
2. Create original **FX 11** icon as `icons/windows.png`.
3. Add a generic/fallback icon and firmware icon.
4. Build the full 1080p `theme.txt` with large menu rows.
5. Implement persistent display names without editing generated `grub.cfg`.
6. Validate all BLS/rescue/UEFI entries.
7. Reboot-test first with Breeze rollback available.
8. Extract this prototype into the future dedicated FX Linux / FX OS repository.
