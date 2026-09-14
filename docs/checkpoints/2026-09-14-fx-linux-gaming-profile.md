# FX Linux gaming profile direction — 2026-09-14

Status: design decision / future implementation. No ISO work in this checkpoint.

## Scope

FX Linux is being developed alongside the LMDE-based FX Live foundation, but remains a separate product direction from FX11.

The gaming stack should be implemented as an optional FX Linux profile / metapackage rather than forced into every installation.

## Restricted media compatibility

Do not import the Ubuntu `ubuntu-restricted-extras` metapackage itself into LMDE/Debian.

Recreate the useful functionality with Debian/LMDE-native packages and clear licensing prompts where required. The Ubuntu Noble metapackage currently pulls/recommends functionality around:

- GStreamer libav
- GStreamer ugly codecs
- VA-API GStreamer support
- FFmpeg extra codecs
- Microsoft core fonts installer
- non-free `unrar`

FX should define a Debian-native equivalent, tentatively `fx-media-extras`, with package-by-package review of availability, licensing and redistribution conditions.

## Gaming launchers

Target launchers / managers for the optional gaming profile:

- Steam
- Heroic Games Launcher
- Lutris
- Bottles

Distribution method should be chosen per application (native package vs Flatpak) based on maintainability and upstream support. Avoid duplicating multiple packaging formats by default.

## SteamOS-inspired optimization direction

Borrow ideas and open-source components from the SteamOS ecosystem; do not copy SteamOS wholesale and do not mix Arch repositories into LMDE/Debian.

Initial candidates:

- GameMode for temporary game-specific CPU / I/O / GPU / scheduler tuning
- gamescope for gaming session / compositor use cases
- current Mesa / Vulkan userspace where safe, preferably through Debian backports or controlled FX packages
- Proton / Wine support stack
- DXVK / VKD3D-Proton where appropriate
- shader-cache handling
- sane power-profile switching during gaming
- NVIDIA hybrid-GPU / PRIME integration through the planned FX Drivers layer

Every optimization must be independently measured and tested. Avoid permanent global "performance" tweaks that increase power use or regress laptops / general desktop use.

## Proposed package/profile split

- `fx-media-extras` — codecs, media compatibility, fonts/archive extras where legally distributable
- `fx-gaming-base` — Vulkan/Wine/Proton support and common runtime prerequisites
- `fx-gaming-tools` — GameMode, gamescope and diagnostics/overlays
- `fx-gaming-launchers` — Steam / Heroic / Lutris / Bottles installation choices
- `fx-gaming` — metapackage selecting the recommended complete gaming profile

Calamares may later expose a simple optional profile choice such as `Gaming support`, while keeping the default FX Linux installation lean.

## Guardrails

- LMDE / Debian remains the base.
- No Ubuntu repository mixing.
- No Arch / SteamOS repository mixing.
- Rebuild or package specific open components only when Debian/LMDE does not provide a suitable version.
- Keep third-party attribution and licensing explicit.
- Gaming optimizations are opt-in and reversible.
