# 2026-09-14 — FX11 Live base direction

Decision: FX11 Live should be built on a reusable Linux base that can later become the technical foundation for a separate FX Linux project, without mixing the two products now.

Provisional preferred base: Debian Stable (currently Debian 13 / Trixie) built with Debian live-build.

Reasons:
- direct upstream base with fewer inherited distribution layers than starting from Linux Mint itself;
- official Debian Live tooling exists and is maintained for Trixie;
- LMDE 7 proves the Linux Mint software stack can run directly on Debian 13, so Mint-like UX remains possible without requiring Ubuntu as the base;
- GParted, parted, sgdisk, GTK and other installer components are readily available;
- the same low-level live/boot/hardware/partitioning platform can later be reused by FX Linux while keeping FX11 Builder and FX Linux as separate repositories/products.

Architecture consequence:
- do not use GParted Live itself as the long-term base OS;
- build an FX-controlled Debian Live image;
- autostart FX11 Installer as the primary application;
- include GParted as a helper tool for Custom partitioning;
- keep WinPE as the Windows deployment engine after the Linux phase;
- if FX Linux is created later, reuse the FX Live base/build tooling in a separate repository and add a full desktop/install target there.

Status: direction selected, implementation not yet started. Base remains subject to validation on real hardware before being called final.
