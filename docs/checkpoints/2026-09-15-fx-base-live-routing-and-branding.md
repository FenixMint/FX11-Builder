# FX Base — Live routing and branding checkpoint (2026-09-15)

## Finalized product flow

All user-visible boot choices start the same FX Base live environment.

- `fx.mode=live` — starts the normal FX Live desktop/tools experience.
- `fx.mode=linux` — starts the same FX Base live environment and additionally launches the FX Linux installation flow using Calamares.
- `fx.mode=windows` — starts the same FX Base live environment and additionally launches the FX11 preparation flow: partitioning, required Windows-install preparation and durable handoff context, then reboot into the FX11 WinPE installer phase for Windows 11 deployment.

The three paths therefore share one live system rather than separate Linux environments.

## FX Base role

FX Base is the common live platform and product foundation for both FX Linux and FX11. It should provide the shared kernel/initrd/root filesystem, hardware/network/storage support, FX branding, FX GRUB/media menu, common tools and the mode router/orchestrator.

## Branding policy

All visible layers are to be FX-branded:

- boot menu / GRUB presentation,
- live desktop and artwork,
- launcher/orchestrator,
- Calamares branding for FX Linux,
- FX11 Linux-side preparation UI,
- FX11 WinPE installer continuation.

The underlying upstream technologies remain credited according to their licenses, but the product presented to the user is FX.

## Architectural consequence

The default design is one kernel, one initrd and one SquashFS for the Linux live stage. Product-specific behavior is selected after boot through `fx.mode` rather than by maintaining multiple separate live systems.

For FX11, the Linux live stage is only phase 1: prepare target storage/context and then reboot into the Windows-based FX11 installer phase. For FX Linux, Calamares performs the Linux installation from the live environment.
