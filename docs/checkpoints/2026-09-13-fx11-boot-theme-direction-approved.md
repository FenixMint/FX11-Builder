# FX11 boot theme direction approved — 2026-09-13

The visual direction for the FX11 boot experience is approved.

Key decisions:
- keep the dark cinematic FX11 direction shown in the approved mockup;
- use the author/project name `Fenix`, not `FenixMint`, in user-facing branding;
- preserve the clean Mint-like usability goal without copying Mint visually;
- target a polished graphical GRUB experience for installation media and later for the installed FX Boot Manager;
- keep the primary installation-media entries simple and user-facing: `FX Partition Manager`, `FX11 Installer`, `Boot existing system`, `UEFI Firmware Settings`;
- avoid developer terminology such as `WinPE fallback` in the visible menu;
- keep `powered by GParted` as secondary attribution rather than part of the main menu title;
- preserve the FX11 visual identity: dark background, restrained green/teal accent, large FX11 mark, translucent menu panels, minimal help text;
- no theme files are considered final until implemented and tested in real GRUB on physical hardware.

Next implementation step after the current boot-path fixes: translate the approved concept into actual GRUB-compatible assets and `theme.txt`, then test at common firmware resolutions before making it the default.
