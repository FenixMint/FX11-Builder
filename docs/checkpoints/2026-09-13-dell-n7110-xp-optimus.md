# Checkpoint — Dell Inspiron N7110 / Windows XP Optimus research

Date: 2026-09-13

This checkpoint records a future legacy-Windows research target. It does not change the current FX11 release priority.

## Reference machine

- Dell Inspiron 17R N7110
- Sandy Bridge generation
- Intel integrated graphics (typically Intel HD Graphics 3000)
- NVIDIA GeForce GT 525M
- NVIDIA Optimus / hybrid graphics

## Research objective

Build a reproducible Windows XP Professional SP3 32-bit compatibility image from user-provided licensed media and determine how far the GT 525M can be made operational on the N7110.

The objective is not satisfied merely by making the NVIDIA device appear in Device Manager. Success levels are tracked separately:

1. GT 525M enumerates.
2. NVIDIA XP driver loads without Code 10/43 or BSOD.
3. NVIDIA control panel/driver identifies the GPU correctly.
4. Direct3D/OpenGL acceleration actually uses the NVIDIA GPU.
5. HDMI/external display works if that connector is physically routed to NVIDIA.
6. NVIDIA-rendered applications can reach the internal LCD.
7. Automatic or manual Optimus-style switching works.

## Current technical hypothesis

The N7110 is believed to use muxless Optimus for the internal panel, with Intel remaining the display owner. NVIDIA officially supported the GT 525M in legacy XP notebook driver families, but NVIDIA Optimus itself was designed for Windows 7 or later. Therefore an INF modification may solve OEM PCI/SUBSYS matching but does not by itself solve the Optimus render/copy/display path.

There are historical reports for the N7110 of a GT 525M PCI identity similar to:

`PCI\VEN_10DE&DEV_0DF5&SUBSYS_04C41028`

This must not be assumed for the user's exact unit. The actual Intel/NVIDIA PCI IDs, SUBSYS IDs and BIOS version must be collected from that machine before creating any driver patch.

A potentially useful hardware path is HDMI if it is physically routed to the NVIDIA GPU. This needs direct verification on the reference machine.

## Planned first test sequence

`XP SP3 x86 -> AHCI/chipset -> Intel graphics -> GT 525M enumeration -> official NVIDIA XP driver + documented INF patch if required -> Direct3D/OpenGL test -> HDMI test -> internal-panel experiments`

## Safety / provenance rules

- Use official NVIDIA, Intel and Dell packages first.
- Record exact package version, original URL and hash.
- If an INF needs modification, preserve the original package and publish the exact patch/diff.
- Clearly mark modified/unsigned drivers.
- Treat XP as a legacy/offline environment by default, not a normal Internet workstation.

## Priority

FX11 remains the active development priority. This N7110 work is saved so the research path is not lost and can resume later without reconstructing the assumptions from chat history.
