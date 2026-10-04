# Repository split notes

The FX family is outgrowing a single builder repository.

This branch intentionally stores the GRUB/FX OS work only as a temporary incubator.

Likely future repository boundaries:

- **FX11-Builder** — reproducible Windows 11 image customization/build tooling.
- **FX-Linux** — Linux system profile, installation/build tooling, COSMIC/Fedora integration and distribution-level configuration.
- **FX-OS-Branding** (or a similarly named shared repo) — common visual identity: GRUB theme, wallpapers, boot artwork, icons and brand assets shared across FX Linux / FX 11.
- **fenix-nightlight** — remains a standalone reusable Linux application.
- **fx-nexus** — remains its own application repository.

Do not move code between repositories until boundaries are clear. For now, use feature/prototype branches and document which files are intended for later extraction.
