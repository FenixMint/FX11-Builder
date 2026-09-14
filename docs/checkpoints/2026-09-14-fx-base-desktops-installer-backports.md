# Checkpoint — FX Base desktops, installer direction and Debian Backports

Date: 2026-09-14

## Confirmed project direction

FX Live / future FX Linux should evolve from an LMDE/Debian-based FX Base rather than GParted Live.

Required or desired components:
- FX Drivers — a Debian-native driver/firmware helper, intended to replace the user-facing gap left by the absence of Mint Driver Manager on LMDE.
- NVIDIA PRIME applet/functionality — desired for hybrid GPU systems.
- Desktop targets for future FX Linux: Cinnamon, MATE, KDE Plasma and TDE (Trinity Desktop Environment).
- Cinnamon remains the natural first/default desktop candidate for the initial FX Live/FX11 entry environment because it best matches the current Mint/LMDE base.

## Installer direction

Installer choice is still open.

Strong requirement: partitioning should feel integrated into the guided installer flow, like Linux Mint/Ubuntu or Calamares, rather than forcing the user through a disconnected external application.

For FX11 specifically:
- Linux Live hosts the FX11 Installer frontend and disk workflow.
- Guided partitioning should be part of the FX11 Installer UI.
- GParted may remain available for advanced/custom partitioning but should not own the install flow.
- after validation, installation continues through WinPE for native Windows deployment tools.

For future FX Linux:
- installer should ideally support the same coherent guided partitioning model and multiple desktop profiles.
- Calamares and Mint/Ubiquity-style integrated partitioning are reference models to evaluate; no final installer choice yet.

## Debian Backports policy for FX

Backports are newer packages taken primarily from Debian Testing and rebuilt for Debian Stable.

They are useful for keeping a stable LMDE/Debian base while selectively introducing newer components such as kernels, firmware, drivers or specific applications.

FX should use backports selectively, not turn the whole stable base into a rolling/testing system.

Intended model:
- stable Debian/LMDE core,
- selected packages from trixie-backports when they materially improve hardware support or required functionality,
- FX packages and configuration on top.

This gives a continuous-release user experience without inheriting the full instability and maintenance burden of Debian Testing as the system base.

## Next validation work

1. Compare installed/live package sets of LMDE 7 Cinnamon and Linux Mint 22.3 Cinnamon.
2. Identify Ubuntu-specific functionality worth recreating or porting rather than importing repositories.
3. Evaluate installer candidates with integrated partitioning, especially Calamares versus a custom Mint/Ubiquity-inspired FX installer flow.
4. Define how Cinnamon, MATE, KDE Plasma and TDE should be shipped: separate images/spins, install-time profiles or meta-packages.
5. Define the first scope of FX Drivers and NVIDIA PRIME integration on Debian/LMDE.
