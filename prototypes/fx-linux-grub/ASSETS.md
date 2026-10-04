# FX OS GRUB prototype assets

## Intended final layout

```text
grub-theme/
├── theme.txt
├── background.png
├── icons/
│   ├── fedora.png
│   ├── windows.png
│   ├── os.png
│   └── uefi.png
├── menu_*.png
├── selected_*.png
├── progress_*.png
└── fonts/
    ├── fxos-regular-24.pf2
    └── fxos-bold-28.pf2
```

## Current validated local artwork

```text
background:
  fxos-grub-background.png
  1920x1080
  SHA256 cd06a7f64c654ca47e2a5c7879418d0e881ef50b9b221215b9803bc4f39ecc95

Fedora class icon:
  fedora.png
  256x256 RGBA
  visual identity: FX Linux Hat
  SHA256 b07395a0c6990252fe4b45e82b43589d5043231ea97ac52bb6978991acc8a14d

Windows class icon:
  windows.png
  256x256 RGBA
  visual identity: FX 11 / window onto the world
  SHA256 9011edce08035aed6e8e57d419706309100815051b6cb9a66347aeace4fb40ea
```

The first real hardware test confirmed that GRUB successfully renders the class icons.

## Current temporary inherited assets

The prototype still inherits Breeze pixmaps for menu and progress rendering:

- `roundedsquare_*.png`
- `progress_bar*.png`
- Unifont fallback files

These are temporary compatibility assets and are not the final FX visual language.

## Fonts

Generated locally with `grub2-mkfont` from static Droid Sans files:

```text
FXOS Regular 24 -> fxos-regular-24.pf2
FXOS Bold 28    -> fxos-bold-28.pf2
```

## Notes

- Wallpaper contains no painted boot-menu entries.
- Real GRUB menu entries are rendered dynamically.
- Fedora kernel updates remain BLS-driven.
- Binary artwork is currently kept local while the visual design is still changing.
- Final binaries will move into the future FX Linux repository when that repository is created.
