# FX OS GRUB Theme Prototype

> Temporary home for the FX Linux / FX OS GRUB work.
>
> This branch is intentionally **not** an FX11 Builder feature branch intended for merge to `main`.
> The theme will be extracted into a dedicated FX Linux repository when the project layout is split.

## Direction

The GRUB implementation follows the proven Linux Mint theme model rather than inventing a custom bootloader mechanism:

- complete standalone theme directory,
- `theme.txt`,
- `background.png`,
- `icons/` with icons selected from GRUB entry classes,
- pixmap assets for menu selection/progress,
- GRUB `.pf2` fonts,
- no menu text painted permanently into the wallpaper,
- no hand-editing generated `grub.cfg`.

## Current target

Primary reference machine:

- Fedora 44 COSMIC
- Lenovo ThinkPad L13 Gen 2
- internal 13-inch 1920x1080 panel
- sometimes used with an external 20-inch 1680x1050 display

The base FX OS theme therefore targets strong readability on the smaller internal display.
A separate 2K/HiDPI variant may be added later, following the same idea as Linux Mint's normal and 2K GRUB themes.

## Known GRUB classes

Current machine:

- Fedora BLS entries: `grub_class fedora`
- Windows Boot Manager: `--class windows --class os`

Planned icons:

- `icons/fedora.png` -> FX Linux Fedora
- `icons/windows.png` -> FX 11
- fallback `icons/os.png`
- later optional firmware/rescue-specific assets if supported cleanly

Fedora kernel updates must continue to work automatically through BLS and the `fedora` class.

## Entries that must remain available

The visual redesign must not remove or hide boot functionality:

- current FX Linux Fedora kernel,
- older Fedora kernels,
- Fedora rescue entry,
- FX 11 / Windows Boot Manager,
- UEFI Firmware Settings.

The primary names may later be presented as:

- **FX Linux Fedora**
- **FX 11**

but naming must be implemented through persistent configuration/generation mechanisms, never by manually editing generated `grub.cfg`.

## Local Fedora prototype path

Current working path on ThinFedora:

```text
/boot/grub2/themes/fxos/
```

The existing Breeze theme remains untouched as rollback:

```text
/boot/grub2/themes/breeze/
```

Current prototype background filename:

```text
background.png
```

## Visual direction

- FX OS planetary landscape background
- dark navy/black base
- blue and warm amber horizon lighting
- large, legible boot menu
- real dynamic GRUB entries over the wallpaper
- 48-56 px class icons in the 1080p variant
- larger text than the Breeze 14/16 px defaults
- selected entry clearly highlighted in FX blue
- controls visible but subordinate to the boot entries

## Extraction plan

This branch is a staging area only.

Expected later split:

- `FX-Linux` or similarly named repository for the Linux system/profile/theme work,
- `FX11` / `FX11-Builder` for Windows-specific work,
- independent repositories for reusable components such as Fenix Night Light.

Do not merge this prototype branch into FX11 Builder `main` as a permanent feature.
